import click

from functools import partial
from kubernetes.config.kube_config import KUBE_CONFIG_DEFAULT_LOCATION
from pathlib import PurePath
import logging
import subprocess
import os
import shutil
import tempfile
import platform #Checkear sistema operativo en el que se está corriendo
from os.path import  expanduser,abspath
from kubernetes.client.rest import ApiException
import kubernetes.client
from kubernetes.config.kube_config import _get_kube_config_loader

from easysparkcli.subcommands.auxiliar.conf import (
    read_config_file,
    validate_raw_config
)
from easysparkcli.subcommands.auxiliar.exceptions import (
    SparkJobError,
    InvalidFilePathError,
    EnvironmentVariableError,
    DriverPodUnsucceeded,
    ArgumentValueError
)

from easysparkcli.subcommands.auxiliar.utils import (
    set_master,
    set_app_name,
    set_container_image,
    set_spark_logging,
    set_executor_memory,
    set_executor_cores,
    set_driver_memory,
    set_driver_cores,
    copy_dir_jars,
    copy_specific_jars,
    copy_specific_libs,
    copy_dir_libs,
    set_executor_instances,
    deploy_mode,
    set_supervise_value,
    mount_sharedpaths_into_pods,
    copy_historyfile
)

submit_deploy_type='cluster' 

#Diccionario para emular sentencia switch-case python y llamar a funcion correspondiente
conf_switcher= {
    'master': partial(set_master),
    'name': partial(set_app_name),
    'container_image': partial(set_container_image),
    'historylogs_dir': partial(set_spark_logging),
    'executor_memory': partial(set_executor_memory),
    'executor_cores' : partial(set_executor_cores),
    'driver_memory' : partial(set_driver_memory),
    'driver_cores' : partial(set_driver_cores),
    'jarsdir' : partial(copy_dir_jars),
    'libs' : partial(copy_specific_libs),
    'jars' : partial(copy_specific_jars),
    'libsdir' : partial(copy_dir_libs),
    'executor_instances' : partial(set_executor_instances),
    #'files' : partial(set_extrafiles),
    #'files_upload_path': partial(set_files_upload_path),
    'supervise': partial(set_supervise_value)
} 

#Recuperar path ejecutable spark-submit usando variables de entorno.
def _get_spark_submit_executable():
    if "SPARK_HOME" not in os.environ:
        raise EnvironmentVariableError("Environment variable SPARK_HOME must be set")
    else:
        sparkhome=PurePath(os.environ["SPARK_HOME"]) #Evitar problemas con el diferente formato de path utilizado en Windows o
        sparkbin= sparkhome / "bin"
        print(sparkbin)
        if os.path.isdir(sparkbin):
            system= platform.system()
            if system == "Windows":
                executable= sparkbin / "spark-submit.cmd"
                if os.access(executable,os.X_OK):
                    return executable
                else:
                    raise EnvironmentError(f"Cannot execute spark-submit.cmd, please check permissions.")          
            else: #Linux o Mac usando mismo ejecutable
                executable= sparkbin / "spark-submit"
                if os.access(executable,os.X_OK):
                    return executable
                else:
                    raise EnvironmentError(f"Cannot execute spark-submit.sh, please check permissions.")
        else:
            raise EnvironmentError(f"Cannot find the path to the spark-submit executable, please check that the environmet variable SPARK_HOME is set properly")

#Eliminamos jars,libs y posibles ficheros logs generados y utilizados para el submit
def _delete_execution_files():

    stringSharedFolder = expanduser("~") #Obtemos path directorio home donde creamos a carpeta a compartir
    sharedFolderPath = PurePath(stringSharedFolder) / ".easySparkTool"

    for filename in os.listdir(sharedFolderPath):
        if filename in ['jars','libs','historylogs'] :
                deleteContentFrom = sharedFolderPath / filename
                if os.path.isdir(deleteContentFrom):
                    try:
                        for file in os.scandir(deleteContentFrom):
                            if file.is_dir():
                                shutil.rmtree(file.path)
                            elif file.is_file():
                                os.unlink(file.path)
                    except Exception as e:
                        print(f'Failure trying to clean current submit execution files. File {file}, reason: {e}')
            
def _process_specified_jar(app_jar,cluster_type):

    fileAppJar = PurePath(app_jar)
    if os.path.isfile(fileAppJar):
        stringSharedFolder = expanduser("~") #Obtemos path directorio home donde creamos a carpeta a compartir
        destinationFilePath = PurePath(stringSharedFolder) / ".easySparkTool" / 'jars' / fileAppJar.name
        shutil.copy(fileAppJar,destinationFilePath)
        if cluster_type == 'k8s':
            k8sAppPath=PurePath("/tmp/sharedpath/jars") / fileAppJar.name
            pathInsideCluster= "local://" + k8sAppPath.as_posix()
            #TODO: Realizar probas, copia de arquivo app realizada.
            return pathInsideCluster
        elif cluster_type == 'standalone':
            standaloneAppPath=PurePath("/vagrant/jars") / fileAppJar.name
            pathInsideCluster= "file://" + standaloneAppPath.as_posix()
            return pathInsideCluster
    else:
        raise ArgumentValueError(f'Application jar {app_jar} was not found in your local system, please check the inserted path')
   
def _format_spark_submit_args(tempfile, cliargs, submitsection,submitExecutablePath,cluster_type):
    argsSubmit=[]
    classValue=cliargs.get("objClass")
    if classValue is None: #Comprobación para dar prioridad a class especificada por terminal.
        classValue=submitsection['class']
    argsSubmit.extend(['--properties-file', tempfile,'--class',classValue])
    argsSubmit.extend(['--deploy-mode','cluster'])
    #Agregar opcions provenientes de línea de comandos
    for key,value in cliargs.items():
        if key=="objClass": #clase ya se ha tratado antes en caso de ser especificado via cli.
            continue
        argsSubmit.extend(["--"+str(key),value])
    #Opción advanced en caso de ser especificada.
    if submitsection.get("advanced") is not None:
        confList=submitsection["advanced"].split(",")
        for conf in confList:
            argsSubmit.extend(conf.split(" "))
    #Agregar jar + jar args
    argsSubmit.append(_process_specified_jar(submitsection.get("app_jar"),cluster_type)) #Só traballamos con arquivos .jar en local, non permitimos outros schemas
    if submitsection.get("app_args") is not None:
        argsFormated = submitsection["app_args"].lstrip().split(' ')
        for arg in argsFormated: 
            argsSubmit.append(arg)
    argsSubmit.insert(0,str(submitExecutablePath)) #Agregamos ejecutable en primera posición
    print(argsSubmit)
    return argsSubmit

def _check_dir_writable(dir):
    """
    Función para comprobar que el directorio en el que guardar el fichero de histórico generado por Spark existe y es válido.
    """
    if os.path.isdir(dir) and os.access(dir,os.W_OK):
        return True
    else:
        return False

def _check_file_writable(file):
    """
    Función para comprobar que los ficheros de salida son válidos y se puede escribir en ellos.
    """
    if os.path.exists(file):
        if os.path.isfile(file):
            return os.access(file,os.W_OK)
        else:
            return False
    dir=os.path.dirname(file)
    return os.access(dir,os.W_OK)

def _retrieve_standalone_logs(drivername, submitconfig):
    outputDestination= submitconfig.get("driverlogs_file")
    home_dir=expanduser("~")
    currentExecutionLogDir = PurePath(home_dir) / ".easySparkTool" / "workDir" / drivername
    stdout = currentExecutionLogDir / "stdout"
    stderr = currentExecutionLogDir / "stderr"
    if outputDestination is None:
        print("*Retrieved logs from the current execution driver process:\n")
        for file in [stderr,stdout]:
            with open(file,'r') as logContent:
                print(logContent.read())
    else:
        destinationFile = PurePath(outputDestination)
        if os.path.isdir(currentExecutionLogDir) and os.path.isfile(stdout) and os.path.isfile(stderr):
            with open(destinationFile,"w") as outputFile:
                for file in [stderr, stdout]:
                    with open(file,"r") as logContent:
                        shutil.copyfileobj(logContent, outputFile)
            print(f"*Driver logs successfully saved to file {destinationFile}.\n")
        else:
            print(f"The driver logs could not be accessed, please check the results from the Spark cluster web interface available at \"https://172.28.128.150:8080\"")
    isHistoryFileRequested = submitconfig.get("historylogs_dir")
    if isHistoryFileRequested is not None:
        print("*Saving history file at " + f"{isHistoryFileRequested} ...\n")
        copy_historyfile(isHistoryFileRequested)

def _retrieve_k8s_logs(validatedconfig, auxPodName, auxNamespace):
    #Conexión a K8s
    configuration = kubernetes.client.Configuration()
    if os.access(expanduser(KUBE_CONFIG_DEFAULT_LOCATION),os.R_OK):#Intentamos coller default conf se existe archivo
        loader= _get_kube_config_loader(filename= KUBE_CONFIG_DEFAULT_LOCATION) #Colle conf da ruta almacenada na variable KUBE_CONFIG_DEFAULT_LOCATION(~/.kube/config)
        loader.load_and_set(configuration)
    #Modificaciones de la configuración especificadas por ususario en el config.file propio
    if validatedconfig.get("k8s") is not None:
        for option,value in validatedconfig["k8s"].items():
            if option in ['api_key','api_key_prefix']:
                getattr(configuration, str(option))["authorization"]=str(value)
                continue
            setattr(configuration, str(option), str(value))
    print("*Trying to connect with kubernetes API ...\n")
    with kubernetes.client.ApiClient(configuration) as api_client: #Auth utiliza por defecto key_file y cert_file, si los borramos y especificamos tokens cambia
        # Create an instance of the API class
        api_instance = kubernetes.client.CoreV1Api(api_client)
        try:
            #print(api_instance.read_namespaced_pod_status_with_http_info(auxPodName,auxNamespace,pretty='true'))         
            respLogs = api_instance.read_namespaced_pod_log(auxPodName, auxNamespace)
            stdoutFile = validatedconfig["submit"].get("driverlogs_file")
            if stdoutFile is None:            
                print("Retrieved logs of the driver pod that executed the spark batch job:\n")
                print(respLogs)
            else:
                outputFile = open(stdoutFile,"w")
                outputFile.write(respLogs)
                outputFile.close()
                print(f"Logs retrieved from K8S had been saved at {stdoutFile}")
            #Comprobación de estado final del Pod para dar aviso en caso de error.
            api_response=api_instance.list_namespaced_pod(auxNamespace)
            for i in api_response.items:
                if i.metadata.name == auxPodName:
                    if i.status.phase != "Succeeded":
                        raise DriverPodUnsucceeded(f"Driver pod {auxPodName} terminates job with a non success status (status = {i.status.phase}), please check logs for detailed info about errors.")
        except ApiException as e:
            print(f"Exception when calling CoreV1Api: {e}\n")
        except IOError as e:
            print(f"Cannot open and write the specified file for K8S logs : {stdoutFile}")
        except DriverPodUnsucceeded as e:
            print(e)
        isHistoryFileRequested = validatedconfig["submit"].get("historylogs_dir")
        if isHistoryFileRequested is not None:
            print("*Saving history file at " + f"{isHistoryFileRequested} ...\n")
            copy_historyfile(isHistoryFileRequested)

def _local_k8s_submit(validatedconfig,file,temppath,cliargs):

    submitExecutablePath = _get_spark_submit_executable()

    mount_sharedpaths_into_pods(file)

    if (validatedconfig["submit"].get("container_image") is None): #Imaxe docker para os contedores por defecto en caso de que usuario non a especifique
        file.write("spark.kubernetes.container.image".ljust(67) + "adrianrc22/spark:latest\n")
    
    if (validatedconfig["submit"].get("jarsdir") is not None) or (validatedconfig["submit"].get("jars") is not None):#Si introducen dependencias Jar, indicamos ruta donde se hace la copia
        file.write("spark.driver.extraClassPath".ljust(67) + "/tmp/sharedpath/jars\n")
        file.write(f"spark.executor.extraClassPath".ljust(67) + "/tmp/sharedpath/jars\n")

    if (validatedconfig["submit"].get("libsdir") is not None) or (validatedconfig["submit"].get("libs") is not None):#Si introducen dependencias como libs, indicamos ruta donde se hace la copia
        file.write("spark.driver.extraLibraryPath".ljust(67) + "/tmp/sharedpath/libs\n")
        file.write(f"spark.executor.extraLibraryPath".ljust(67) + "/tmp/sharedpath/libs\n")

    for key,value in validatedconfig["submit"].items():
        if key in ["app_jar","app_args","advanced","class",'driverlogs_file']:
            continue
        elif key in ["jarsdir","libsdir","libs","jars"]:
            conf_switcher.get(key)(value)
        elif key in ["historylogs_dir"]:
            conf_switcher.get(key)(file,'k8s')
        else:
            conf_switcher.get(key)(file, value)
    argsSubmit=_format_spark_submit_args(temppath,cliargs,validatedconfig["submit"],submitExecutablePath,'k8s')
    print("\n" + str(argsSubmit) + "\n")
    file.seek(0)
    print("\n*Executing apache spark batch job ...\n")
    try:
        pcs=subprocess.run(argsSubmit,text=True,capture_output=True)
        pcs.check_returncode()
    except subprocess.CalledProcessError as e:
        raise SparkJobError(
        "Error during the execution of the spark-submit command:\n {0}".format(pcs.stderr))
    #Recuperamos info pod creado para recuperar sus logs posteriormente 
    auxPodName=pcs.stderr.partition("pod name: ")[2].split("\n")[0] #Recuperamos pod name
    auxNamespace=pcs.stderr.partition("namespace: ")[2].split("\n")[0] #Recuperamos pod name   
    _retrieve_k8s_logs(validatedconfig, auxPodName, auxNamespace)

def _local_standalone_submit(validatedconfig, file, temppath, cliargs):

    submitExecutablePath = _get_spark_submit_executable()
    if (validatedconfig["submit"].get("jarsdir") is not None) or (validatedconfig["submit"].get("jars") is not None):#Si introducen dependencias Jar, indicamos ruta donde se hace la copia
        file.write("spark.driver.extraClassPath".ljust(67) + "/vagrant/jars\n")
        file.write(f"spark.executor.extraClassPath".ljust(67) + "/vagrant/jars\n")

    if (validatedconfig["submit"].get("libsdir") is not None) or (validatedconfig["submit"].get("libs") is not None):#Si introducen dependencias como libs, indicamos ruta donde se hace la copia
        file.write("spark.driver.extraLibraryPath".ljust(67) + "/vagrant/libs\n")
        file.write(f"spark.executor.extraLibraryPath".ljust(67) + "/vagrant/libs\n")

    for key,value in validatedconfig["submit"].items():
        if key in ["app_jar","app_args","advanced","class",'driverlogs_file']:
            continue
        elif key in ["jarsdir","libsdir","libs","jars"]:
            conf_switcher.get(key)(value)
        #Función habilitar logs necesita saber con que cluster estamos a traballar xa que cambian rutas internasd    
        elif key in ["historylogs_dir"]:
            conf_switcher.get(key)(file,'standalone')
        else:
            conf_switcher.get(key)(file, value)
    
    argsSubmit=_format_spark_submit_args(temppath,cliargs,validatedconfig["submit"], submitExecutablePath,'standalone')
    file.seek(0)
    print("\n*Executing apache spark batch job ...\n")
    try:
        pcs=subprocess.run(argsSubmit,text=True,capture_output=True)
        pcs.check_returncode()
    except subprocess.CalledProcessError:
        raise SparkJobError(
        "Error during the execution of the spark-submit command:\n {0}".format(pcs.stderr))
    driverName = pcs.stderr.partition("Driver successfully submitted as ")[2].split("\n")[0] #Recuperamos driver name
    #print(driverName)
    print("*Retrieving submit driver logs ...\n")
    _retrieve_standalone_logs(driverName, validatedconfig["submit"])

@click.command()
@click.option('--configfile','-cf',required=True,type=click.Path(exists=True,resolve_path=True,readable=True), help="Configuration file path")
def cli(**kwargs):
    '''
    Subcommand to send batch jobs to Spark Cluster and retrieve execution results.
    '''
    rawconfig= read_config_file(abspath(kwargs['configfile'])) #Lectura del archivo de configuración
    validatedconfig = validate_raw_config(rawconfig) #Validacion de la configuracion usando el esquema

    #Controlar que exista sección Submit
    #if validatedconfig.get("submit") is None:
    #    raise submitSectionMustExist("Submit section is required in the configuration file for the execution of this subcommand. Please rewrite the specified configuration file.")
    
    #Variable controlar si guardamos logs k8s en fichero salida o no
    cluster_type=validatedconfig["cluster"]["deploy_type"]
    
    #Validacion fichero de salida a escribir
    driver_output_file= validatedconfig["submit"].get("driverlogs_file")
    if (driver_output_file is not None) and not (_check_file_writable(driver_output_file)):
        raise InvalidFilePathError("The specified file to write the driver output is not valid, please check path permissions or if it exists.")

    #Validacion directorio destino fichero history
    historydir_path = validatedconfig["submit"].get("historylogs_dir")
    if (historydir_path is not None) and not (_check_dir_writable(historydir_path)):
        raise InvalidFilePathError("The specified directory to save the history file is not valid, please check path permissions or if it exists.") 

    cliargs={}
    for arg,value in kwargs.items():
        if (value is not None) and (arg not in ['configfile']):
            #arg=arg.replace("_","-")  #Cambiar 
            # os, ya que kwargs devuelve con _ y necesitamos -. deploy_mode -> deploy-mode       
            cliargs.update({arg:value}) #agrega campo nuevo con el par de valores
    
    #TODO: Revisar Try-catch-finally
    try:
        fd, temppath = tempfile.mkstemp(suffix=".conf",text=True)
        with os.fdopen(fd, "r+") as file:
            deploy_mode(file,submit_deploy_type) #HARDCODEADO, NON PERMITIMOS MODO CLIENT EN ESTA APROXIMACIÓN, TRABAJO FUTURO.
            if cluster_type == 'k8s':
                _local_k8s_submit(validatedconfig,file, temppath, cliargs)
            elif cluster_type == 'standalone':
                _local_standalone_submit(validatedconfig,file,temppath,cliargs)
            print("* The submit operation has been successfully completed! You can check the results from the web interface or, depending on how the output was configured, through the CLI.\n")
    finally:
        _delete_execution_files() #Limpamos ficheiros utilizados pola actual execución
        os.unlink(temppath)
    
    
from typing import Text
import click
import logging
import subprocess
import shutil
import time
import sys
import json
import vagrant
import yaml
import os
from pathlib import PurePath
from functools import partial
from os.path import abspath, expanduser

from easysparkcli.subcommands.auxiliar.exceptions import (
    MinikubeExecutableNotFoundError,
    VagrantExecutableNotFoundError,
    ClusterSetupError,
    RequiredSectionError,
    sharedFolderPermissionsError
)

from easysparkcli.subcommands.auxiliar.utils import (
    set_minikube_cpus,
    set_minikube_provider,
    set_minikube_memory
)

from easysparkcli.subcommands.auxiliar.conf import (
    read_config_file,
    validate_raw_config
)

switcherOptions = {
    'node_cpus': partial(set_minikube_cpus),
    'node_memory': partial(set_minikube_memory),
    'provider': partial(set_minikube_provider)
}

VAGRANTFILE_CONTENT= r"""require 'yaml'
USERCONFIG = YAML.load_file(File.join(File.dirname(__FILE__), 'config.yml'))

Vagrant.configure("2") do |config|
  N_WORKERS = USERCONFIG["workers"]

  config.vm.box = "ubuntu/bionic64"

  #config.vm.synced_folder USERCONFIG["managedSharedFolder"], "/localsharedfolder"    

  config.vm.define "spark-Master" do |node|
    ipVm="172.28.128.150"
    node.vm.hostname = "spark-Master"
    node.vm.network "private_network", ip: ipVm

    node.vm.provider "virtualbox" do |vb|
        vb.name = "spark-Master"
        vb.gui = false
        vb.memory = USERCONFIG["node_memory"]
        vb.cpus = USERCONFIG["node_cpus"]
    end

    node.vm.provision "shell", inline: <<-SHELL 
        apt-get install -y python-dev avahi-daemon default-jdk
        wget -O /vagrant/spark.tgz https://downloads.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
        mkdir /home/vagrant/spark
        tar xf /vagrant/spark.tgz -C /home/vagrant/spark --strip 1
        chown -R vagrant:vagrant /home/vagrant/spark
        echo "export SPARK_HOME=/home/vagrant/spark" >> /home/vagrant/.bashrc
        echo "export PATH=$PATH:/home/vagrant/spark/bin" >> /home/vagrant/.bashrc
        #echo "spark.master spark://172.28.128.150:7077" >> /home/vagrant/spark/conf/spark-defaults.conf
        echo "SPARK_MASTER_HOST=172.28.128.150" >> /home/vagrant/spark/conf/spark-env.sh
        sudo sed -i 's/^127.\\+//' /etc/hosts
        echo "127.0.0.1 localhost" >> /etc/hosts   
        #Crear clave ssh
        USER_DIR=/home/vagrant/.ssh
        echo -e 'y\n' | sudo -u vagrant ssh-keygen -t rsa -f $USER_DIR/id_rsa -q -N ''
        if [ ! -f $USER_DIR/id_rsa.pub ]; then
            echo "SSH public key could not be created"
            exit -1
        fi
        chown vagrant:vagrant $USER_DIR/id_rsa*
        cp $USER_DIR/id_rsa.pub /vagrant
        if [ ! -f /vagrant/id_rsa.pub ]; then
            echo "SSH public key could not be copied"
            exit -1
        fi
        # Copiar clave ssh pública para permitir ssh passwordless
        USER_DIR=/home/vagrant/.ssh
        if [ ! -f /vagrant/id_rsa.pub ]; then
            echo "SSH public key does not exist"
            exit -1
        fi
        sed -i "/-aisi/d" .ssh/authorized_keys >& /dev/null
        cat /vagrant/id_rsa.pub >> $USER_DIR/authorized_keys
        chown vagrant:vagrant $USER_DIR/authorized_keys
        chmod 0600 $USER_DIR/authorized_keys >& /dev/null
    SHELL

    node.vm.provision :shell, path: "setupConnectivity+Worker.sh", args: [USERCONFIG["workers"], ipVm]
  end

  (0..N_WORKERS-1).each do |i|
    config.vm.define "spark-Worker#{i}" do |node|
      ipVm="172.28.128.20#{i}"
      node.vm.hostname = "spark-Worker#{i}"
      node.vm.network "private_network", ip: ipVm

      node.vm.provider "virtualbox" do |vb|
        vb.name = "spark-Worker#{i}"
        vb.gui = false
        vb.memory = USERCONFIG["node_memory"]
        vb.cpus = USERCONFIG["node_cpus"]
      end

      node.vm.provision "shell", inline: <<-SHELL
        apt-get install -y python-dev avahi-daemon default-jdk
        mkdir /home/vagrant/spark
        tar xf /vagrant/spark.tgz -C /home/vagrant/spark --strip 1
        chown -R vagrant:vagrant /home/vagrant/spark
        echo "export SPARK_HOME=/home/vagrant/spark" >> /home/vagrant/.bashrc
        echo "export PATH=$PATH:/home/vagrant/spark/bin" >> /home/vagrant/.bashrc
        echo SPARK_MASTER_HOST=172.28.128.150 >> /home/vagrant/spark/conf/spark-env.sh 
        # Copiar clave ssh pública para permitir ssh passwordless
        USER_DIR=/home/vagrant/.ssh
        if [ ! -f /vagrant/id_rsa.pub ]; then
            echo "SSH public key does not exist"
            exit -1
        fi
        sed -i "/-aisi/d" .ssh/authorized_keys >& /dev/null
        cat /vagrant/id_rsa.pub >> $USER_DIR/authorized_keys
        chown vagrant:vagrant $USER_DIR/authorized_keys
        chmod 0600 $USER_DIR/authorized_keys >& /dev/null
      SHELL
      workerMemory = USERCONFIG["node_memory"] + "m"
      node.vm.provision :shell, path: "setupConnectivity+Worker.sh", args: [USERCONFIG["workers"], ipVm, USERCONFIG["node_cpus"], workerMemory, "worker"]
    end
  end
end
"""

CONNECTIVITY_SCRIPT_CONTENT = '''\
#!/bin/bash
sudo sed -i 's/^127.\\+//' /etc/hosts
echo "127.0.0.1 localhost" >> /etc/hosts 
i=0
nodes=$(( $1 - 1 ))

while [ $i -le $nodes ] 
do
    echo "172.28.128.20$i spark-Worker$i" >> /etc/hosts
    i=$(( $i + 1 ))
done

if [ "$5" = "worker" ]; then
    echo $4
    /home/vagrant/spark/sbin/start-worker.sh -h $2 -c $3 -m $4 -d /vagrant/workDir spark://172.28.128.150:7077 
else
    /home/vagrant/spark/sbin/start-master.sh -h $2
fi
'''

#Función usada tanto en despregue standalone como k8s para comprobar que a carpeta que se xestiona internamente se pode crear
def purgeDefaultSharedFolder(sharedpath):

    if os.path.isdir(sharedpath):
        if not os.access(sharedpath, os.W_OK):
            raise sharedFolderPermissionsError(f"Folder managed by sparkbatchtool, {sharedpath} must have write permissions for current user, please delete it or change current permissions.")
        #Borramos posibles residuos de anterior setup de cluster
        for filename in os.listdir(sharedpath):
            file_path= os.path.join(sharedpath, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)       
    
def set_yml_cpus(clustersection, dict):

    cpus = clustersection.get("node_cpus")
    if cpus is None:
        dict["node_cpus"]=1 #Default 1 cores
    else:
        dict["node_cpus"]=cpus

def set_yml_memory(clustersection,dict):

    memory = clustersection.get("node_memory")
    if memory is None:
        dict["node_memory"]="2048" #Default 2gb memory
    else:
        dict["node_memory"]=str(memory)

def set_yml_workers(clustersection,dict):

    workers = clustersection.get("workers")
    if workers is None:
        dict["workers"]=1 #Default 1 worker node
    else:
        dict["workers"]=workers

def set_yml_shareddir(dict):

    homedir = expanduser("~")
    sharedpath = PurePath(homedir) / ".easySparkTool"
    dict["managedSharedFolder"]=sharedpath.as_posix() #Punto montaxe carpeta compartida xestionada pola ferramenta.


def get_vagrantfile_variables(clustersection):

    dict= {}
    set_yml_cpus(clustersection,dict)
    set_yml_memory(clustersection,dict)
    set_yml_workers(clustersection,dict)
    set_yml_shareddir(dict)
    return dict

def prepare_shared_folder(sharedpath,standalone):

    if not os.path.isdir(sharedpath):
        os.mkdir(sharedpath)
    else:
        purgeDefaultSharedFolder(sharedpath)

    libspath = sharedpath / "libs"
    jarspath = sharedpath  / "jars"
    historypath = sharedpath / "historylogs"
    if not os.path.isdir(jarspath):
        os.mkdir(jarspath.as_posix())
    
    if not os.path.isdir(libspath):
        os.mkdir(libspath.as_posix())
    
    if not os.path.isdir(historypath):
        os.mkdir(historypath.as_posix())
    
    #Directorio que se utilizará para el espacio de memoria y los registros de salida de los trabajos
    if standalone:
        workpath = sharedpath / "workDir"
        if not os.path.isdir(workpath):
            os.mkdir(workpath.as_posix())

def local_standalone_deploy(clustersection):
    if shutil.which("vagrant") is None:
        raise VagrantExecutableNotFoundError("Vagrant is required and executable could not be found, please install the software or check environment variables.") 
    #Creación directorio temporal sobre o que traballará vagrant almacenando Vagrantfile e config.yaml coas variables.
    stringSharedFolder = expanduser("~") #Obtemos path directorio home donde creamos a carpeta a compartir
    sharedpath = PurePath(stringSharedFolder) / ".easySparkTool"
    prepare_shared_folder(sharedpath,True)
    #if not os.path.isdir(sharedpath):
    #    os.mkdir(sharedpath)
    #else:
    #    purgeDefaultSharedFolder(sharedpath)
    configymlpath = sharedpath / "config.yml"
    #Create yaml file for variables used in vagrantfile
    with open(configymlpath,"w", encoding="utf-8") as yaml_file:
        print(clustersection)
        dict = get_vagrantfile_variables(clustersection)
        yaml.dump(dict,yaml_file,default_flow_style=False)
    bashScriptDirPath = sharedpath / "setupConnectivity+Worker.sh"
    #Create bash script for configure connectivity between cluster nodes
    with open(bashScriptDirPath,'w') as bashscript:
        bashscript.write(CONNECTIVITY_SCRIPT_CONTENT)
    #Create vagrantfile for cluster deploy
    vagrantfiledirpath = sharedpath / "Vagrantfile"
    with open(vagrantfiledirpath,"w", encoding="utf-8") as vagrant_file:
        vagrant_file.write(VAGRANTFILE_CONTENT)
        vagrant_file.write("\n")   
    #Levantar entorno standalone con Vagrant
    #pcsVagrantUp = subprocess.run(['vagrant','up'],stderr=sys.stderr,stdout=sys.stdout, cwd=sharedpath)
    envvars = os.environ.copy()
    envvars["VAGRANT_CWD"] = str(sharedpath)
    v = vagrant.Vagrant(env=envvars,quiet_stdout=False,quiet_stderr=False)
    try:
        v.up()
    except:
        print("\n* ERROR: Cluster could not be deployed successfully, please check previous logs to see the problems. Proceeding to remove the cluster dependencies to return to a consistent state ... ") 
        v.destroy()
        exit()
    print(f"\n* Completed! Information summary to interact with the cluster:\n\n\t+ Spark Standalone Master waiting for submit jobs at \"spark://172.28.128.150:7077\"\n\n\t+ Spark Standalone Cluster WebUI availiable at \"http://172.28.128.150:8080\"")


#Configuración cluster Kubernetes a levantar, especificando valores por defecto recomendados por Spark
def addMinikubeArgs(clustersection):

    cmd = ['minikube', 'start','-p','EasySpark'] #TODO: Testear despliegue con provider vbox e non docker
    
    if clustersection.get("node_cpus") is not None:
        cmd.extend(['--cpus',str(clustersection["node_cpus"])])
    else:
        cmd.extend(['--cpus',str(3)])
    
    if clustersection.get("node_memory") is not None:
        cmd.extend(['--memory',str(clustersection["node_memory"])])
    else:
        cmd.extend(['--memory',str(4096)])

    #if clustersection.get("provider") is not None:
    #    cmd.extend(['--driver',str(clustersection["provider"]),'--no-vtx-check'])
    #else:
    cmd.extend(['--driver','docker'])

    return cmd

def local_k8s_deploy(clustersection):

    if shutil.which("minikube") is None:
        raise MinikubeExecutableNotFoundError("Minikube is required and executable could not be found, please install the software or check environment variables.") 
    
    minikubeStatusCmd = ['minikube','status', '-p', 'Easy']
    pcsStatus = subprocess.run(minikubeStatusCmd,capture_output=True)

    #Devuelve 85 si encuentra perfil minikube (perfiles son usados para correr distintas instancias minikube)
    if pcsStatus.returncode == 85:           
        print(f"* Checking for possible minikube profiles with name \"EasySpark\" ...\n")                
        #Comprobar estado actual del perfil  con el que se trabaja actualmente (actualProfile) para dar aviso en caso de Running
        pcsProfilesList = subprocess.run(['minikube', 'profile', 'list','-o','json'], capture_output=True)
        json_profiles_list=pcsProfilesList.stdout
        profilesListAsDict=json.loads(json_profiles_list)
        for category,list in profilesListAsDict.items():
            if category == "valid":
                for profile in list:
                    profileName=profile["Name"]
                    if  profileName != "EasySpark":   
                        continue               
                    else:
                        update=input(f"\n* A local kubernetes cluster with the specified profile name \"EasySpark\" already exists (use \"minikube profile list\" for extended info).  Do you want to delete the current existing cluster and create a new one? (Y/n):    ")
                        while update.lower() not in ['','y','n']:
                            update = input("Please, insert y/n to response:    ")
                            break
                        if update.lower() == 'n':
                            print("\n* Stopping create subcommand ...\n")
                            exit()
                        else:
                            print("\n* Deleting old kubernetes cluster for Spark ...")
                            cmd=['minikube','delete','-p','EasySpark']
                            subprocess.run(cmd,stderr=sys.stderr,stdout=sys.stdout)
                    break

    print("* Deploying local k8s cluster ...")
    minikubeExec = addMinikubeArgs(clustersection)
    #for option,value in clustersection.items():
    #    if option != "deploy_type":
    #        switcherOptions.get(option)(minikubeExec,value)
            
    stringSharedFolder = expanduser("~") #Obtemos path directorio home donde creamos a carpeta a compartir
    sharedpath = PurePath(stringSharedFolder) / ".easySparkTool"
    prepare_shared_folder(sharedpath,False)
    
    mountstring = '--mount-string=' + sharedpath.as_posix() + ":/localsharedfolder"
    minikubeExec.extend(['--mount', mountstring])
    pcsStart = subprocess.run(minikubeExec,stderr=sys.stderr,stdout=sys.stdout)

    if pcsStart.returncode != 0:
        raise ClusterSetupError("Unsuccess K8s cluster setup, please check the output of the command to see the problem.")

    print("\n* Configuring service account default:default with required privilegies on default namespace for execute spark jobs ...\n")
    pcsServiceAccount = subprocess.run(['kubectl', 'create', 'clusterrolebinding', 'default', '--clusterrole=edit', '--serviceaccount=default:default', '--namespace=default'],text=True,capture_output=True)                
    
    if pcsServiceAccount.returncode != 0:
        print(f"   -{pcsServiceAccount.stderr}")
    
    print("* Configuring Web K8S Dashboard: Execute \"kubectl proxy\" command to make dashboard avaliable at http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/ ...\n")
    pcsDashboard = subprocess.run(['kubectl', 'apply', '-f', 'https://raw.githubusercontent.com/kubernetes/dashboard/v2.2.0/aio/deploy/recommended.yaml'],text=True,capture_output=True)       
    
    if pcsDashboard.returncode != 0:
        print(f"    -{pcsDashboard.stderr}")
    
    print("* Retrieving Access Token for K8s Dashboard ...\n")
    pcsClusterInfo = subprocess.run(['kubectl', 'cluster-info'],text=True,capture_output=True)
    ctrlPlaneDns=pcsClusterInfo.stdout.split("\n")
    pcsAccessToken = subprocess.run(['kubectl','-n','kube-system','describe','secret','default'],text=True,capture_output=True)
    #Ejecutado al momento de hacer el start no recupera los token de acceso, detecta como que no se crearon los recursos.
    if pcsAccessToken.returncode ==0:
        for line in pcsAccessToken.stdout.splitlines():
                if line.startswith("token:"):
                    bearerToken = str.strip(line.partition("token:")[2])
        print(f"* Completed! Information summary to interact with the cluster:\n\n\t+ {ctrlPlaneDns[0]}\n\n\t+ {ctrlPlaneDns[1]}\n\n\t+ Execute \"kubectl proxy\" to make Kubernetes Dashboard avaliable at: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/\n\n\t+ Bearer Token (Kuberentes Web Dashboard Authentication):     {bearerToken}\n")
    else:    
        print("* Waiting cluster resources to be ready...")
        seconds=3
        maxAttempts = 1
        while pcsAccessToken.returncode != 0 and maxAttempts <= 5:#4 intentos
            print(f"\t Attempt {maxAttempts} ...")
            time.sleep(seconds)
            seconds+=2
            maxAttempts+=1
            pcsAccessToken = subprocess.run(['kubectl','-n','kube-system','describe','secret','default'],text=True,capture_output=True)
        if pcsAccessToken.returncode != 0:
            print(f"\n* Completed! Information summary to interact with the cluster:\n\n\t+ {ctrlPlaneDns[0]}\n\n\t+ {ctrlPlaneDns[1]}\n\n\t+ Execute \"kubectl proxy\" to make Kubernetes Dashboard avaliable at: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/\n\n\t+ Bearer Token (Kberentes Web Dashboard Authentication):     ERROR: Couldn't retrieve access token in this moment, try later with \"kubectl -n kube-system describe secret default\n")
        else:    
            for line in pcsAccessToken.stdout.splitlines():
                if line.startswith("token:"):
                    bearerToken = str.strip(line.partition("token:")[2])
            print(f"\n* Completed! Information summary to interact with the cluster:\n\n\t+ {ctrlPlaneDns[0]}\n\n\t+ {ctrlPlaneDns[1]}\n\n\t+ Execute \"kubectl proxy\" to make Kubernetes Dashboard avaliable at: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/\n\n\t+ Bearer Token (Kuberentes Web Dashboard Authentication):     {bearerToken}\n")

@click.option('--configfile','-cf',required=True,type=click.Path(exists=True), help="Path to the configuration file")
@click.command()
def cli(**kwargs):
    """
    Deploys a local Spark cluster to which batch jobs may be sent for execution.
    """
    try:

        rawconfig= read_config_file(abspath(kwargs['configfile'])) #Lectura del archivo de configuración
        validatedconfig = validate_raw_config(rawconfig) #Validacion de la configuracion usando el esquema
        
        if "cluster" in validatedconfig.keys():
            if validatedconfig["cluster"]["deploy_type"] == 'k8s':
                local_k8s_deploy(validatedconfig["cluster"])
            elif validatedconfig["cluster"]["deploy_type"] == 'standalone':
                local_standalone_deploy(validatedconfig["cluster"])
            #TODO:else:
                #cloud_deploy(validatedconfig["cluster"])
        else:           
            raise RequiredSectionError("   To execute the subcommand \"clusterinit\" it is necessary to specify a configuration file in which the \"cluster\" section exists with at least all its required fields.")    
    
    except KeyboardInterrupt:
        logging.error("""
WARNING: execution interrupted by the user!
Your clusters may be in inconsistent state!
""")

    except OSError as err:
        logging.error(err)

    except Exception as e:
        logging.error(e)
    



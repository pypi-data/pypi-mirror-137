from schema import Schema,SchemaError,Or,Optional
from configparser import ConfigParser
from os.path import expandvars
import sys,os

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easysparkcli.subcommands.auxiliar.exceptions import ConfigfileValidationError

from easysparkcli.subcommands.auxiliar.validations import (
    existing_file,
    nonempty_str,
    url,
    positive_int,
    memory_units,
    master_url,
    check_advanced,
    app_jar,
    booleanCheck
)

#TODO: Meter comprobaciones bien en cada tipo: tipos,regex...
SCHEMA= {
    'submit' : {
        Optional(str): str
    },
    'k8s': {
        Optional('ssl_ca_cert') : existing_file,
        Optional('api_key') : nonempty_str,
        Optional('api_key_prefix') : nonempty_str,
        Optional('host') : url,
        Optional('username'): nonempty_str,
        Optional('password'): nonempty_str,
        Optional('verify_ssl'): booleanCheck,
        Optional('cert_file'): existing_file,
        Optional('key_file'): existing_file,
        Optional('retries'): positive_int
    },
    'cluster': {
        'deploy_type': Or("k8s","standalone"),
        Optional(str): str
    }
}

SUBMIT_APP_SCHEMAS = {
    'k8s': {
        'master': master_url,
        'class': nonempty_str,
        'app_jar': app_jar,
        Optional('container_image'):nonempty_str,
        Optional('app_args'): nonempty_str,
        Optional('name'): nonempty_str,     
        Optional('jarsdir'):nonempty_str,
        Optional('jars'):nonempty_str,
        Optional('libsdir'):nonempty_str,
        Optional('libs'):nonempty_str,
        Optional('driver_memory'):memory_units,
        Optional('driver_cores'):positive_int,
        Optional('executor_memory'):memory_units,
        Optional('executor_cores'):positive_int,
        Optional('executor_instances'): positive_int,
        Optional('historylogs_dir'):nonempty_str,
        Optional('advanced'):check_advanced,
        Optional('driverlogs_file'):  nonempty_str,
    },
    'standalone': {
        'master': master_url,
        'class': nonempty_str,
        'app_jar': app_jar,
        Optional('app_args'): nonempty_str,
        Optional('name'): nonempty_str,      
        Optional('jarsdir'):nonempty_str,
        Optional('jars'):nonempty_str,
        Optional('libsdir'):nonempty_str,
        Optional('libs'):nonempty_str,
        Optional('driver_memory'):memory_units,
        Optional('driver_cores'):positive_int,
        Optional('executor_memory'):memory_units,
        Optional('executor_cores'):positive_int,
        Optional('executor_instances'): positive_int,
        Optional('historylogs_dir'):nonempty_str,
        Optional('advanced'):check_advanced,
        Optional('supervise'): booleanCheck,    
        Optional('driverlogs_file')   : nonempty_str 
    }
}

CLUSTER_TYPE_SCHEMAS = {
    'k8s': {
        "deploy_type": "k8s",
        Optional('node_cpus'): positive_int,
        Optional('node_memory'): positive_int,
        #Optional('provider'): Or('docker','virtualbox'), #'kvm2','vmware','parallels','hyperkit','none','hyperv','ssh'
    },
    'standalone': {
        "deploy_type": "standalone",
        Optional('workers'): positive_int,
        Optional('node_memory'): positive_int,
        Optional('node_cpus'): positive_int
    }
}
def read_config_file(filepath):
    '''
    Leer las opciones de ejecución del fichero de configuración especificado en la opción --config
    '''
    cfg= ConfigParser()
    cfg.read(filepath)
    config={}
    for section in cfg.sections():
        config[section] = {}
        for key in cfg.options(section):
            value = cfg.get(section, key)
            #Revisar, cfg.get serviría para extender valores iniciados por %() como pasa en windows
            config[section][key] = expandvars(value)
    return config

def validate_cluster_section(newconfig):
    """
    Ejecutar validación con schema correspondiente según tipo cluster solicitado
    """
    type = newconfig["deploy_type"]
    return Schema(CLUSTER_TYPE_SCHEMAS[type]).validate(newconfig)

def validate_submit_section(newconfig):
    """
    Ejecutar validación con schema correspondiente según tipo de cluster contra el que se realiza el submit
    """
    type = newconfig["cluster"]["deploy_type"]
    return Schema(SUBMIT_APP_SCHEMAS[type]).validate(newconfig["submit"])

def validate_raw_config(rawconfig):
    """
    Función para validar el fichero de configuración usando el schema.
    """
    
    newconfig = {}
    #Validamos primero siempre sección cluster, ya que de esta sección depende el modelo de submit a aplicar
    data = rawconfig.get("cluster")
    try:

        if data is not None:
                modelClusterSection = SCHEMA['cluster']
                newconfig["cluster"] = Schema(modelClusterSection).validate(data)
                newconfig["cluster"] = validate_cluster_section(newconfig['cluster'])
        else:
            raise ConfigfileValidationError('Section \'cluster\' must exist in the configuration file. Please, rewrite it')  

        for section,model in SCHEMA.items():
            if section not in rawconfig or section == 'cluster':
                continue
            data = rawconfig[section]
            newconfig[section] = Schema(model).validate(data)

            if section == 'submit':
                newconfig[section] = validate_submit_section(newconfig)

    except (SchemaError, ValueError) as error:
                raise ConfigfileValidationError(f'    ERROR validating the specified configuration file: \n{error}')

    return newconfig
    
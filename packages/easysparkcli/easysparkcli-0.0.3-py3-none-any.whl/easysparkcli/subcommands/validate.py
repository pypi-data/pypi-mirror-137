import click

from pathlib import PurePath
from os.path import  abspath
from schema import SchemaError, Schema
from functools import partial
from easysparkcli.subcommands.auxiliar.exceptions import ConfigfileValidationError, validationError
from easysparkcli.subcommands.auxiliar.conf import (
    read_config_file,
    SCHEMA,
    SUBMIT_APP_SCHEMAS,
    CLUSTER_TYPE_SCHEMAS,
    validate_raw_config
)

def validate_k8s_section(configcontent):
    k8s_section=configcontent.get("k8s")
    aux={}
    if k8s_section is not None:
        model_k8s_schema=SCHEMA["k8s"]
        aux["k8s"] = Schema(model_k8s_schema).validate(k8s_section)
    else:
        raise ConfigfileValidationError(f'* Section \"k8s\" was not found in the current configuration file. Please, check it')

def validate_submit_section(configcontent):
    submit_section=configcontent.get("submit")
    aux={}
    if submit_section is not None:
        model_submit_section=SCHEMA["submit"]
        aux["submit"] = Schema(model_submit_section).validate(submit_section)
        type=configcontent.get("cluster")["deploy_type"].lower()
        if type is None:
            raise validationError("* In order to validate the submit option, there must be a well-formed \"cluster\" section in the specified file to know the type of cluster with which you want to work.")
        if type in ["k8s","standalone"]:
            Schema(SUBMIT_APP_SCHEMAS[type]).validate(aux["submit"])
        else:
            raise validationError(f"* At \"cluster\" section, \"deploy_type\" key with value \"{type}\" is not valid. In order to validate the submit option, there must be a well-formed \"cluster\" section in the specified file to know the type of cluster with which you want to work.")
    else:
        raise ConfigfileValidationError(f'* Section \"submit\" was not found in the current configuration file. Please, check it')

def validate_cluster_section(configcontent):
    cluster_section= configcontent.get("cluster")
    aux={}
    if cluster_section is not None:
        model_cluster_section = SCHEMA['cluster']
        aux["cluster"] = Schema(model_cluster_section).validate(cluster_section)
        type = aux["cluster"]["deploy_type"]
        Schema(CLUSTER_TYPE_SCHEMAS[type]).validate(aux["cluster"])
    else:
        raise ConfigfileValidationError(f'* Section \"cluster\" was not found in the current configuration file. Please, check it.')

switch_validations = {
    'k8s': partial(validate_k8s_section),
    'cluster': partial(validate_cluster_section),
    'submit': partial(validate_submit_section)
}

@click.option("--section",'-s',multiple=True,help="Specify a specific section to validate. If not provided, the entire configfile will be validated.")
@click.argument('configfile', nargs=1,type=click.Path(exists=True,resolve_path=True,readable=True))
@click.command()
def cli(**kwargs):
    """
    This option allow users to validate configuration file before using it.
    """
    cfgfilepath=PurePath(abspath(kwargs['configfile']))
    sections=kwargs.get("section")
    rawconfig= read_config_file(str(cfgfilepath)) #Lectura del archivo de configuración
    if len(sections) == 0:
        try:
            validate_raw_config(rawconfig) #Validacion de la configuracion completa usando el esquema
            print(f"\n* Specified configuration file \"{cfgfilepath}\" was successfully validated!\n")
        except (SchemaError, ValueError) as error:
            raise ConfigfileValidationError(f'* ERROR validating the speficied configuration file: \n{error}')
    else:
        sectionsList=list(set(sections))
        for sectionName in sectionsList:
            if sectionName  in ["k8s","submit","cluster"]:
                switch_validations.get(sectionName)(rawconfig)      
            else:
                sectionsList.remove(sectionName)
                print(f"* Specified section {sectionName} is not supported at the Scheme validation and is not used by the CLI,  skipping it ...\n")
        if len(sectionsList)==1:
            print(f"\n* Section {sectionsList} of the specified configuration file \"{cfgfilepath}\" was successfully validated!\n")
        elif len(sectionsList)>1:
            print(f"\n* Sections {sectionsList} of the specified configuration file \"{cfgfilepath}\" were successfully validated!\n")
                
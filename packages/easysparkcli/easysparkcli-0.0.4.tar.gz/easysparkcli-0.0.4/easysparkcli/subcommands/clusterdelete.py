import shutil
import subprocess
import logging
import sys
import click
import vagrant
import os

from pathlib import PurePath
from os.path import expanduser

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easysparkcli.subcommands.auxiliar.exceptions import deleteClusterError
from easysparkcli.subcommands.auxiliar.conf import (
    read_config_file,
    validate_raw_config
)



@click.option('--configfile','-cf',required=True,type=click.Path(exists=True), help="Path to the configuration file")
@click.command()
def cli(**kwargs):
    """
    Deletes deployed on-premise Spark cluster and its associated files.
    """
    try:
        x=suma(1,2)
        print(x)
        stringSharedFolder = expanduser("~")       
        sharedpath = PurePath(stringSharedFolder) / ".easySparkTool"
        raw_data=read_config_file(kwargs.get("configfile"))
        validated_data=validate_raw_config(raw_data)

        if validated_data["cluster"].get("deploy_type") == 'k8s':
            cmd=['minikube','delete','-p','EasySpark']
            subprocess.run(cmd,stderr=sys.stderr,stdout=sys.stdout)

        elif validated_data["cluster"].get("deploy_type") == 'standalone':
            envvars = os.environ.copy()
            envvars["VAGRANT_CWD"] = str(sharedpath)
            v = vagrant.Vagrant(env=envvars,quiet_stdout=False,quiet_stderr=False)
            #Comprobamos que exista algún entorno, si no existe vagrant status ya devuelve error
            try:
                v.status()
            except:
                print("\n")
                raise deleteClusterError(f" Can't remove cluster, no Standalone deployment made with the EasySpark tool has been found.")
            v.destroy()  
            print("* Cluster Standalone successfully deleted!\n")

        if os.path.isdir(sharedpath):
            shutil.rmtree(sharedpath, ignore_errors=True)

    except KeyboardInterrupt as err:
        logging.error("""
WARNING: execution interrupted by the user!
Your clusters may be in inconsistent state!
""")
    except Exception as e:
        logging.error(e)

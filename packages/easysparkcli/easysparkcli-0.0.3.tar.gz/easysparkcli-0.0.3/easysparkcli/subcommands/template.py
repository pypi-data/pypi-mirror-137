import configparser
import click
from pathlib import PurePath

INTRO= '''# EasySparkTool Configuration Template
# ====================================
#
# This is a TEMPLATE CONFIGURATION file for EasySparkTool.  You will
# need to edit it and replace some placeholder values before the file
# can be read without errors and you can actually start creating
# Apache Spark clusters and submitting applications to it.\n
#
#
# The sections and required configuration values for execution are uncommented,
# while the optional fields are commented.
#
# ====================================


'''
@click.option('--folderdest','-f',type=click.Path(exists=True,resolve_path=True,writable=True,dir_okay=True, file_okay=False), help="Existing directory in which to save the sample.ini configuration file model.")
@click.command()
def cli(**kwargs):
    """
    Creates a sample .ini file with all the available options for the tool to be used as a template.
    """
    try:
        if kwargs.get('folderdest') is not None:
            file_path= str(PurePath(kwargs['folderdest']) / 'sample.ini')
        else:
            file_path='sample.ini'
        with open(file_path,'w') as samplefile:
            samplefile.write(INTRO)
            templateCfg = configparser.ConfigParser(allow_no_value=True)
            samplefile.write(';Mandatory section, used both to start/destroy the cluster and to run a job\n')
            templateCfg['cluster'] = {'deploy_type' : '# k8s OR standalone',
                                    '; ------- note: Optional values for both deploy_types' : None,
                                    'node_cpus' : '#Default: 2 for Standalone mode, 3 for Kubernetes mode',
                                    'node_memory' : '#Default: 2048 for Standalone mode, 4096 for Kubernetes mode',
                                    '; ------- note: Optional values for standalone deploy_type':None,
                                    'workers' : '#Default: 1'
                                    }
            templateCfg.write(samplefile)
            templateCfg.clear()
            #TODO: Submit section obligatorio para facer clusterinit/clusterdelete
            samplefile.write(';Mandatory section for submit subcommand\n')
            templateCfg['submit'] = {'; ------- note: Required options for submit execution' : None,
                                    'master': '#https://172.28.128.150:7077 for Standalone deploy, k8s://https://127.0.0.1:XXXX for K8s deploy',
                                    'class' : '#application main class',
                                    'app_jar' : '#Path to the bundled jar that includes the application and its dependencies.',
                                    '':None,
                                    '; ------- note: Optional values for both deploy_types, k8s and standalone.' : None,
                                    'app_args' : '#Arguments passed to the main method of the main class, if any.',
                                    'name' : '#Name to show at UI and log data for the application.',
                                    'jarsdir' :'#Existing local directory path containing possible extra jars needed for the execution of the application.',
                                    'jars' : '#Existing local jars paths needed for the execution of the app, separated by commas.',
                                    'libsdir' : '#Existing local directory path containing possible extra libs needed for the execution of the application.',
                                    'libs' : '#Existing local libs paths needed for the execution of the app, separated by commas.',
                                    'driver_memory' : '#Amount of memory to use for driver process, specified with JVM memory format. Examples: 1g,512m, 1024k.',
                                    'driver_cores' : '#Driver process number of cores to use, positive integer.',
                                    'executor_memory' : '#Amount of memory to use per executor process, specified with JVM memory format. Examples: 1g,512m, 1024k.',
                                    'executor_instances' : '#Positive integer to specify number of executor process used to run the job.',
                                    'logs_dir' : '#Local path to store the log file after the application execution in case the enable_logs options has value true. Useful for reconstructing the process with a Apache Spark History Server.',
                                    'enable_logs' : '#Whether to generate a log file of the app execution with Spak events, if not specified the value is false.',
                                    'historylogs_dir' : '#Directory path where to save the history file.',
                                    'driverlogs_file' : '#File path where to save the driver logs. If not specified, logs are shown as submit output in console.',
                                    'advanced' : '#Option that allows you to specify extra configuration options as if you were using the original submit, with the format --conf spark.XXX.XXX=XXX. Accepts several comma-separated options.',
                                    '':None,
                                    '; ------- note: Optional value only for k8s deploy_type.' : None,
                                    'container_image' : '#Container image to use for the Spark application. if not specified, a default one is used.',
                                    '':None,
                                    '; ------- note: Optional value only for standalone deploy_type.' : None,
                                    'supervise' : '#Boolean value. If its set to True, application execution is restarted automatically if it exited with non-zero exit code. By default its value is false.',
                                    }
            templateCfg.write(samplefile)
            templateCfg.clear()

            samplefile.write(';Optional section in case of k8s deploy_type, customize  used K8S client to retrieve results of the submit. By default, client is configured with ~/kube/.config/ files.\n#')
            templateCfg["k8s"] = {'ssl_ca_cert' : 'Set this to customize the certificate file to verify the peer.',
                                'api_key' : '#Provide a specific API Key. ',
                                'api_key_prefix' : '#Prefix to the specific API Key, default: Bearer.',
                                'host' : '#Base url to connect to.',
                                'username' : '#Username for HTTP basic authentication.',
                                'password' : '#Password for HTTP basic authentication.',
                                'verify_ssl' : '#Set this to false to skip verifying SSL certificate when calling API from https server. Default value is true.',
                                'cert_file' : '#Customize the certificate file to verify the peer.',
                                'key_file' : '#Client key file.',
                                'retries' : '#Allowed client connection attempts, default value 3.'
                                }
            
            templateCfg.write(samplefile)
        if file_path == 'sample.ini':
            print('Successfully generated template config file \'sample.ini\' in the current directory')
        else:
            print(f'Successfully generated template config file \'sample.ini\' at {file_path}')
    except Exception as e:
        print(e)


# EasySpark

EasySpark aims to make easier for users the execution of batch jobs with Apache Spark framework. It provides a user-friendly command line tool to create, setup and manage on-premise Spark clusters and ease the execution of batch jobs against those deployed clusters. 

Its main objective is to facilitate the whole process of running batch jobs in Spark, providing subcommands to deploy/delete the necessary infrastructure and submit the desired jobs to that infraestructure.

The EasySpark project supports multiple operating systems (Windows, MacOS and Linux) and is open source licensed under the GNU General Public License v3. 

## Features
Easyspark CLI receives parameters via .INI configuration files, and offers the following functionalities:

* Setup and manage on-premise Spark clusters.
* Easy batch job submission to Spark clusters.

In order to facilitate the use of the mentioned features, the CLI tool has subcommands that allow validating and creating .INI configuration files with the accepted parameters.

## Software Requirements

It is mandatory to have Apache Spark downloaded on the workstation and the _SPARK_HOME_ environment variable correctly configured.

Additionally, depending on the requested cluster manager for the Spark cluster, it will be necessary:

* Standalone Spark cluster:
    * Minikube
    * Docker
* Kubernetes Spark cluster:
    * VirtualBox
## Installation

Run the following to install:

```python
pip install easySparkTool
```

## Installation from source

Clone EasySpark's repository from GitHub. Next open a terminal,  `cd` into that path and run:

```console
pip install -e .
```

## Quick Start

> Usage: ```easysparkcli COMMAND [ARGS]```

Once installed, you can check the different options of the tool through the command:

```console
easysparkcli --help
```

EasySpark counts with 5 subcommands:

1. template
    * Creates, as a template, a .INI configuration file with all the available options for the tool.
2. validate
    * Validates the provided .INI configuration file, checking if it meet the requirements.
3. clusterinit
    * Create and setup on-premise Spark Cluster using Kubernetes or Spark Standalone as cluster manager to be able to execute batch jobs on this infraestructure.
4. clusterdelete
    * Deletes Spark clusters previously deployed with EasySpark and its associated files.
5. submit 
    * Allows users to submit batch jobs to the Spark cluster in a more user-friendly manner
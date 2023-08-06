#! /usr/bin/env python

from setuptools import setup, find_packages

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    ]

REQUIREMENTS = [
    "click >= 8.0.3",
    "schema >= 0.7.5",
    "configparser >= 5.2.0",
    "kubernetes >= 21.7.0",
    "python_vagrant >= 0.5.15",
    "pyyaml >= 0.0.2",
    ]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'easysparkcli',
    version = '0.0.4',
    author = 'Adrian Rodriguez Couto',
    author_email = 'adrian.rcouto@udc.es',
    description="Command Line Tool created with the purpose of ease the use of Apache Spark, allowing users to deploy/delete a Spark Cluster and submit batch jobs easily through different options.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(),
    python_requires ='>=3.6',
    classifiers =CLASSIFIERS,
    install_requires = REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'easysparkcli = easysparkcli.__main__:main'
        ]
    },
    keywords = 'spark python cli package automation automice deployment',
)
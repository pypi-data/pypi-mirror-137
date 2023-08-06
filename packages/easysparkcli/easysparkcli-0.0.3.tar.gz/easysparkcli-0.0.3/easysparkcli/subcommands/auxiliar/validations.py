#! /usr/bin/python

from multiprocessing import Value
import os
import schema
import re
from pathlib import PurePath
from urllib.parse import urlparse

def string_to_boolean(word):
    """
    Función para permitir flexibilidad en el fichero de configuración a la hora de especificar si se activan los logs o no,
    permitiendo los valores true,yes,on o 1(sin diferencia de minúsculas y mayúsculas) para indicar verdadero, en cualquier
    otro caso los logs recibirán el valor False"""
    if word.strip().lower() in ['true', 'yes', 'on', '1']:
        return True
    else:
        return False

booleanCheck = schema.Use(string_to_boolean)

def validator(fn):
    """
    Decorate a function for use as a validator with `schema`_

    .. _schema: https://github.com/keleshev/schema
    """
    return schema.Use(fn)

def _file_name(v):
    try:
        return os.path.expanduser(v)
    except Exception as err:
        raise ValueError("invalid file name `{0}`: {1}".format(v, err))


@validator
def existing_file(v):
    print("K")
    f = _file_name(v)
    if os.access(f, os.F_OK):
        return f
    else:
        raise ValueError("file `{v}` could not be found".format(v=v))

@validator
def nonempty_str(v):
    converted = str(v)
    if not converted:
        raise ValueError("value must be a non-empty string")
    return converted

@validator
def url(value):
    try:
        url_str = str(value)
        urlparse(url_str)
        return url_str
    except Exception as err:
        raise ValueError("Invalid URL `{0}`: {1}".format(value, err))

@validator
def positive_int(v):
    converted = int(v)
    if converted > 0:
        return converted
    else:
        raise ValueError("value must be integer > 0")

@validator
def master_url(url):
    pattern= re.compile(r'\w:([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
    if bool(re.search(pattern,url)):
        return url
    else:
        raise ValueError(f"Specified master url {url} is not valid. This option uses HTTPS by default if it is not specificated and must include a number port between 1 and 65535. Example -> https://localhost:8856")

@validator
def app_jar(jar):
    pattern=re.compile(r'\w(.jar)$')
    if bool(re.search(pattern,jar)):
        if os.access(jar, os.F_OK):
            return jar
        else:
            raise ValueError(f"file `{jar}` could not be found")
    else:
        raise ValueError(f"Specified application jar {jar} is not valid. Inserted value must have .jar extension.")

@validator
def memory_units(units):
    pattern= re.compile(r"[1-9][0-9]*([k,m,g,t])$")
    if bool(re.search(pattern,units)):
        return units
    else:
        raise ValueError(f"The specified value {units} for memory config is not valid. Write it as JVM memory string format, using one of the following size unit suffix: k (Kilobyte), m (Megabyte), g (Gigabyte) or t (Terabyte). Example -> 512m")

@validator
def check_advanced(advanced):
    pattern= re.compile(r"^(--conf) (spark\.[A-Za-z.]+=[A-Za-z0-9999]+)(,--conf spark\.[A-Za-z.]+=[A-Za-z0-9]+)*$")
    if bool(re.search(pattern,advanced)):
        return advanced
    else: 
        raise ValueError(f"Specified value: {advanced} for key \"advanced\" in configfile is not valid. Please, rewrite it using the right sintax (whitespace as separator between confs): --conf spark.xxx=xxx")   

@validator
def check_files(files):
    pattern=re.compile(r"^([A-Za-z0-9:\\/._-]+)(,[A-Za-z0-9:\\/._-]+)*$")
    if bool(re.search(pattern,files)):
        return files
    else:
        raise ValueError(f"Files key of the specified config file is not valid: {files}. Should be one or more paths to local file or URLs globally visible inside the cluster, separated by commas. Example:  file:///path/to/some/file.conf,")

@validator
def check_valid_mkdir_path(path):
    if os.path.isdir(path):
        if os.access(path,os.W_OK):
            return path
        else:
            raise ValueError(f"Specified folder it nos writable. Please, change folder permissions or specify a different folder.")
    elif os.path.isdir(os.path.dirname(path)):
        if os.access(os.path.dirname(path),os.W_OK):
            return path
        else:
            raise ValueError(f"Specified folder it nos writable. Please, change folder permissions or specify a different folder.")
    else:
        raise ValueError(f"Specified folder to save cluster files cannot be found. Specifiy and existing directory or atleast an existing dirname at the pathname")

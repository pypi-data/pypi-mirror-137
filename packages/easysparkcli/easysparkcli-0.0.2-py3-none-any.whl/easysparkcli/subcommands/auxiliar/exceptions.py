#! /usr/bin/env python

class SparkJobError(Exception):
    pass

class ConfigfileValidationError(Exception):
    pass

class InvalidFilePathError(Exception):
    pass

class EnvironmentVariableError(Exception):
    pass

class DriverPodUnsucceeded(Exception):
    pass

class MinikubeExecutableNotFoundError(Exception):
    pass

class VagrantExecutableNotFoundError(Exception):
    pass
class ArgumentValueError(Exception):
    pass

class ClusterSetupError(Exception):
    pass

class RequiredSectionError(Exception):
    pass

class sharedFolderPermissionsError(Exception):
    pass

class submitSectionMustExist(Exception):
    pass

class invalidURLSchemeAppJar(Exception):
    pass

class validationError(Exception):
    pass

class deleteClusterError(Exception):
    pass
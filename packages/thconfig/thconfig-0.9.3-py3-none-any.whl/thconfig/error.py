__all__ = ['ConfigError', 'FileConfigError', 'CouchConfigError']

from thresult import ResultException


class ConfigError(ResultException):
    pass


class FileConfigError(ConfigError):
    pass


class CouchConfigError(ConfigError):
    pass

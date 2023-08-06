__all__ = ['FileConfig', 'FileConfigResult']

import os
import toml
import yaml
import json
import json5

from os.path import splitext
from typing import Any
from toml.decoder import TomlDecodeError
from yaml.scanner import ScannerError

from thresult import Ok, Err
from thconfig.config import Config
from thconfig.error import FileConfigError


FileConfigResult: type = Ok[bool] | Err[Any]


class FileConfig(Config):
    '''
    A class to handle reading and writing configuration data from file
    '''
    _path: str
    _fetch: bool
    _commit: bool
    _state: dict
    _file_ext: str


    def __init__(self, path: str, fetch: bool=True, commit: bool=False):
        self._path = path
        self._fetch = fetch
        self._commit = commit
        self._state = {}
        self._file_ext = self.__parse_file_extension()


    def __setattr__(self, attr: str, value: Any):
        '''
        Stores object's attributes
        '''
        if attr in ('_path', '_fetch', '_commit', '_state', '_file_ext'):
            self.__dict__[attr] = value
        else:
            self.__dict__['_state'][attr] = value


    def __parse_file_extension(self) -> str:
        '''
        Returns file extension
        '''
        _, ext_ = splitext(self._path)
        return ext_[1:]


    @FileConfigResult[bool, FileConfigError | TomlDecodeError |  ValueError | ScannerError]
    async def fetch(self) -> bool:
        '''
        Reads config data from file
        '''
        if not os.path.exists(self._path):
            raise FileConfigError(f'Path not found {self._path!r}')
        
        with open(self._path) as f:
            match self._file_ext:
                case 'toml':
                    self._state = toml.load(f)
                case 'yaml':
                    self._state = yaml.safe_load(f)
                case 'json':
                    self._state = json.load(f)
                case 'json5':
                    self._state = json5.load(f)
                case _:
                    raise FileConfigError(f'Unsupported file extension, '
                                          f'expected toml, yaml, json or json5 file, got {self._file_ext}')

        return True


    @FileConfigResult[bool, FileConfigError | TypeError]
    async def commit(self) -> bool:
        '''
        Write config data to file
        '''
        with open(self._path, 'w') as f:
            match self._file_ext:
                case 'toml':
                    toml.dump(self._state, f)
                case 'yaml':
                    yaml.dump(self._state, f)
                case 'json':
                    json.dump(self._state, f)
                case 'json5':
                    json5.dump(self._state, f)
                case _:
                    raise FileConfigError(f'Unsupported file extension, '
                                          f'expected toml, yaml, json or json5 file, got {self._file_ext}')
        
        return True

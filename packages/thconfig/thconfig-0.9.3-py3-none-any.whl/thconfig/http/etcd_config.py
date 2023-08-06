__all__ = ['EtcdConfig']

import json
import aetcd3

from typing import Any

from .http_config import HTTPConfig
from thresult.result import Ok, Err


EtcdConfigResult: type = Ok[bool] | Err[Any]


class EtcdConfig(HTTPConfig):
    '''
    A class to handle reading and writing configuration data from etcd
    '''
    _host: str
    _port: int
    _fetch: bool
    _commit: bool
    _state: dict


    def __init__(self, host: str, port: int, fetch: bool=True, commit: bool=False):
        self._host = host
        self._port = port
        self._fetch = fetch
        self._commit = commit
        self._state = {}
    

    def __setattr__(self, attr: str, value: Any):
        '''
        Stores object's attributes
        '''
        if attr in ('_host', '_port', '_fetch', '_commit', '_state'):
            self.__dict__[attr] = value
        else:
            self.__dict__['_state'][attr] = value


    @EtcdConfigResult[bool, OSError | TypeError]
    async def fetch(self) -> bool:
        '''
        Fetching document and store data in self._state
        Sync etcd -> self._state
        https://aetcd3.readthedocs.io/en/latest/reference/client.html#aetcd3.client.Etcd3Client.get_all
        '''
        async with aetcd3.client(self._host, self._port) as client:
            self._state = {}

            async for v, meta in client.get_all():
                k: str = meta.key.decode()
                v: str = json.loads(v.decode())
                self._state[k] = v
        
        return True
         
    
    @EtcdConfigResult[bool, AttributeError]
    async def commit(self) -> bool:
        '''
        Commit document, save data from self._state to etcd
        Sync self._state -> etcd
        https://aetcd3.readthedocs.io/en/latest/reference/client.html#aetcd3.client.Etcd3Client.put
        '''
        async with aetcd3.client(self._host, self._port) as client:
            for k, v in self._state.items():
                v: str = json.dumps(v)
                await client.put(k, v)
        
        return True

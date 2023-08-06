__all__ = ['CouchConfig', 'CouchConfigResult']

from typing import Any
from urllib.parse import urlparse

from aiohttp import ClientSession
from thconfig.error import CouchConfigError
from thresult.result import Ok, Err

from .http_config import HTTPConfig


CouchConfigResult: type = Ok[bool] | Err[Any]


class CouchConfig(HTTPConfig):
    '''
    A class to handle reading and writing configuration data from couchdb
    '''
    _uri: str
    _fetch: bool
    _commit: bool
    _state: dict


    def __init__(self, uri: str, fetch: bool=True, commit: bool=False):
        self._uri = uri
        self._fetch = fetch
        self._commit = commit
        self._state = {}


    def __setattr__(self, attr: str, value: Any):
        '''
        Stores object's attributes
        '''
        if attr in ('_uri', '_fetch', '_commit', '_state'):
            self.__dict__[attr] = value
        else:
            self.__dict__['_state'][attr] = value
            

    @CouchConfigResult[bool, CouchConfigError | ValueError]
    async def fetch(self) -> bool:
        '''
        Fetching document and store data in self._state
        Sync couchdb -> self._state
        https://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
        '''
        self._state = {}         
        async with ClientSession() as session:
            # parse db_name and doc_id
            p = urlparse(self._uri)
            _, db_name, doc_id = p.path.split('/')

            # try create database
            uri = f'{p.scheme}://{p.netloc}/{db_name}'

            async with session.put(uri) as resp:
                # assert resp.status in (201, 202, 412)
                # res = await resp.json()
                match resp.status:
                    case 201 | 202 | 412:
                        await resp.json()
                    case 400:
                        raise CouchConfigError(f'Invalid database name: \'{db_name}\'')
                    case 401:  # pragma: no cover
                        raise CouchConfigError('Unauthorized – CouchDB Server Administrator privileges required')
                    case _:  # pragma: no cover
                        raise CouchConfigError(f'Unknown Status Error: {resp.status}')

            # get document
            async with session.get(self._uri) as resp:
                # assert resp.status in (200, 404)
                #
                # if resp.status == 200:
                #     self._state = await resp.json()
                # else:
                #     self._state = {}
                match resp.status:
                    case 200:
                        self._state = await resp.json()
                    case 404:
                        self._state = {}
                    case 400:  # pragma: no cover
                        raise CouchConfigError('The format of the request or revision was invalid')
                    case 401:  # pragma: no cover
                        raise CouchConfigError('Unauthorized – Read privilege required')
                    case _:  # pragma: no cover
                        raise CouchConfigError(f'Unknown Status Error: {resp.status}')

        return True
                

    @CouchConfigResult[bool, CouchConfigError | ValueError]
    async def commit(self) -> bool:
        '''
        Commit document, save data from self._state to couchdb
        Sync self._state -> couchdb
        https://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid
        '''
        async with ClientSession() as session:
            # parse db_name and doc_id
            p = urlparse(self._uri)
            _, db_name, doc_id = p.path.split('/')

            # try create database
            uri = f'{p.scheme}://{p.netloc}/{db_name}'

            async with session.put(uri) as resp:
                # assert resp.status in (201, 202, 412)
                # res = await resp.json()
                match resp.status:
                    case 201 | 202 | 412:
                        await resp.json()
                    case 400:
                        raise CouchConfigError(f'Invalid database name: \'{db_name}\'')
                    case 401:  # pragma: no cover
                        raise CouchConfigError('Unauthorized – CouchDB Server Administrator privileges required')
                    case _:  # pragma: no cover
                        raise CouchConfigError(f'Unknown Status Error: {resp.status}')


            # get latest config document
            rev = None

            async with session.get(self._uri) as resp:
                # assert resp.status in (200, 404)
                # data = await resp.json()
                # if resp.status == 200:
                #     rev = data['_rev']
                match resp.status:
                    case 200:
                        data = await resp.json()
                        rev = data['_rev']
                    case 404:
                        # data = await resp.json()
                        pass
                    case 400:  # pragma: no cover
                        raise CouchConfigError('The format of the request or revision was invalid')
                    case 401:  # pragma: no cover
                        raise CouchConfigError('Unauthorized – Read privilege required')
                    case _:  # pragma: no cover
                        raise CouchConfigError(f'Unknown Status Error: {resp.status}')

            # put config document
            uri = self._uri

            if rev:
                uri = f'{uri}?rev={rev}'

            doc = {
                k: v
                for k, v in self._state.items()
                if k not in ('_id', '_rev')
            }

            async with session.put(uri, json=doc) as resp:
                # assert resp.status in (201, 202)
                # res = await resp.json()
                match resp.status:
                    case 200 | 201:
                        await resp.json()
                    case 400:  # pragma: no cover
                        raise CouchConfigError('Bad Request – Invalid request body or parameters')
                    case 401:  # pragma: no cover
                        raise CouchConfigError('Unauthorized – Write privileges required')
                    case 404:  # pragma: no cover
                        raise CouchConfigError('Not Found – Specified database or document ID doesn’t exists')
                    case 409:  # pragma: no cover
                        raise CouchConfigError('Conflict – Document with the specified ID already exists or specified')
                    case _:  # pragma: no cover
                        raise CouchConfigError(f'Unknown Status Error: {resp.status}')
                
        return True
        

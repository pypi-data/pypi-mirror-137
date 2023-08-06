[![Build][build-image]]()
[![Status][status-image]][pypi-project-url]
[![Stable Version][stable-ver-image]][pypi-project-url]
[![Coverage][coverage-image]]()
[![Python][python-ver-image]][pypi-project-url]
[![License][bsd3-image]][bsd3-url]


# thconfig

## Overview
TangledHub library for config with a focus on asynchronous functions

## Licensing
thconfig is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details

## Installation
```bash
pip install thconfig
```

---

## Testing
```bash
docker-compose build thconfig-test ; docker-compose run --rm thconfig-test
```

## Building
```bash
docker-compose build thconfig-build ; docker-compose run --rm thconfig-build
```

## Publish
```bash
docker-compose build thconfig-publish ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thconfig-publish
```


## THCONFIG supported in this library
...

## Testing
```python
docker-compose build thconfig-test ; docker-compose run --rm thconfig-test
```

## Usage

### File 
Configuration from file 

#### setup
```python
'''
A class to handle reading and writing configuration data from file
'''

# you need to provide file with data { configuration }
config_path = 'example_1.json'

# create instance of FileConfig
config = FileConfig(config_path)
```

#### fetch
```python
'''
Reads config data from file
'''

# you need to provide file with data { configuration }
config_path = 'example_1.json'

# create instance of FileConfig
config = FileConfig(config_path)

# load data from configuration file if success
res: bool = (await config.fetch()).unwrap()
```

#### commit
```python
'''
Write config data to file
'''

# you need to provide file with data { configuration }
config_path = 'example_1.json'

# create instance of FileConfig
config = FileConfig(config_path)

# set title
config['title'] = 'Config Example'

config.title2 = 'Config Example'

# this function change title in file
(await config.commit()).unwrap()
```

### CouchConfig 
Configuration from couchdb 

#### setup
```python
'''
A class to handle reading and writing configuration data from couchdb

instantiate CouchConfig:
        parameters:
            uri: str
'''

# this is url for couchdb where are configuration data 
URI = 'http://tangledhub:tangledhub@couchdb-test:5984/thconfig-test/test_couch_config'

# create intance CouchConfig and set URI property
config = CouchConfig(URI)
```

#### fetch
Fetching configuration document from couchdb
```python
'''
Fetching document and store data in self._state
Sync couchdb -> self._state
https://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid

Fetch:
    parameters:
        self: CouchConfig
'''

# this is url for couchdb where are configuration data 
URI = 'http://tangledhub:tangledhub@couchdb-test:5984/thconfig-test/test_couch_config'

# create intance CouchConfig and set URI property
config = CouchConfig(URI)

# fetching data from database
fetched_data = (await config.fetch()).unwrap()
```

#### commit
Commit changes in configuration data in documment in couchdb
```python
'''
Commit document, save data from self._state to couchdb
Sync self._state -> couchdb
https://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid

Commit:
    parameters:
        self: CouchConfig
'''

# this is url for couchdb where are configuration data 
URI = 'http://tangledhub:tangledhub@couchdb-test:5984/thconfig-test/test_couch_config_commit_changes'

# create intance CouchConfig and set URI property
config = CouchConfig(URI)

title = 'Couch Config Example'
database = {'server': '192.168.1.1'}

# set title and database
config['title'] = title
config['database'] = database

# commit
commit_0 = (await config.commit()).unwrap()
```

### EtcdConfig 
Configuration from EtcdConfig 

#### setup
```python
'''
A class to handle reading and writing configuration data from etcd
instantiate EtcdConfig:
    parameters:
        HOST: str
        PORT: int
'''

# you need to provide host and port
HOST = 'etcd-test'
PORT = 2379

# create instance of EtcdConfig
config = EtcdConfig(host = HOST, port = PORT)
```

#### fetch
Fetching configuration document from etcd
```python
'''
Fetching document and store data in self._state
Sync etcd -> self._state
https://aetcd3.readthedocs.io/en/latest/reference/client.html#aetcd3.client.Etcd3Client.get_all

Fetch:
    parameters:
        self: EtcdConfig
'''

# you need to provide host and port
HOST = 'etcd-test'
PORT = 2379

# create instance of EtcdConfig
config = EtcdConfig(host = HOST, port = PORT)

# fetching data from etcd
fetched_data = (await config.fetch()).unwrap()
```

#### commit
Commit changes in configuration data to etcd
```python
'''
Commit document, save data from self._state to etcd
Sync self._state -> etcd
https://aetcd3.readthedocs.io/en/latest/reference/client.html#aetcd3.client.Etcd3Client.put

commit changes:
    parameters:
        self: EtcdConfig
'''

# you need to provide host and port
HOST = 'etcd-test'
PORT = 2379

# create instance of EtcdConfig
config = EtcdConfig(host = HOST, port = PORT)

title = 'Couch Config Example'
database = {'server': '192.168.1.1'}

# set title and database
config['title'] = title
config['database'] = database

# commit
commit_0 = (await config.commit()).unwrap()
```

<!-- Links -->

<!-- Badges -->
[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause
[build-image]: https://img.shields.io/badge/build-success-brightgreen
[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green

[pypi-project-url]: https://pypi.org/project/thquickjs/
[stable-ver-image]: https://img.shields.io/pypi/v/thquickjs?label=stable
[python-ver-image]: https://img.shields.io/pypi/pyversions/thquickjs.svg?logo=python&logoColor=FBE072
[status-image]: https://img.shields.io/pypi/status/thquickjs.svg



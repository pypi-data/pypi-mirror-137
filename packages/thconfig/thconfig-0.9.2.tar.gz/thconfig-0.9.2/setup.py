# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thconfig', 'thconfig.file', 'thconfig.http']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aetcd3>=0.1.0a7.post1,<0.2.0',
 'aiohttp>=3.81,<4.0',
 'json5>=0.9.6,<0.10.0',
 'thresult>=0.9.0,<0.10.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'thconfig',
    'version': '0.9.2',
    'description': 'TangledHub Config reader/writter',
    'long_description': "[![Build][build-image]]()\n[![Status][status-image]][pypi-project-url]\n[![Stable Version][stable-ver-image]][pypi-project-url]\n[![Coverage][coverage-image]]()\n[![Python][python-ver-image]][pypi-project-url]\n[![License][bsd3-image]][bsd3-url]\n\n\n# thconfig\n\n## Overview\nTangledHub library for config with a focus on asynchronous functions\n\n## Licensing\nthconfig is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details\n\n## Installation\n```bash\npip install thconfig\n```\n\n---\n\n## Testing\n```bash\ndocker-compose build thconfig-test ; docker-compose run --rm thconfig-test\n```\n\n## Building\n```bash\ndocker-compose build thconfig-build ; docker-compose run --rm thconfig-build\n```\n\n## Publish\n```bash\ndocker-compose build thconfig-publish ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thconfig-publish\n```\n\n\n## THCONFIG supported in this library\n...\n\n## Testing\n```python\ndocker-compose build thconfig-test ; docker-compose run --rm thconfig-test\n```\n\n## Usage\n\n### File \nConfiguration from file \n\n#### setup\n```python\n'''\nA class to handle reading and writing configuration data from file\n'''\n\n# you need to provide file with data { configuration }\nconfig_path = 'example_1.json'\n\n# create instance of FileConfig\nconfig = FileConfig(config_path)\n```\n\n#### fetch\n```python\n'''\nReads config data from file\n'''\n\n# you need to provide file with data { configuration }\nconfig_path = 'example_1.json'\n\n# create instance of FileConfig\nconfig = FileConfig(config_path)\n\n# load data from configuration file if success\nres: bool = (await config.fetch()).unwrap()\n```\n\n#### commit\n```python\n'''\nWrite config data to file\n'''\n\n# you need to provide file with data { configuration }\nconfig_path = 'example_1.json'\n\n# create instance of FileConfig\nconfig = FileConfig(config_path)\n\n# set title\nconfig['title'] = 'Config Example'\n\nconfig.title2 = 'Config Example'\n\n# this function change title in file\n(await config.commit()).unwrap()\n```\n\n### CouchConfig \nConfiguration from couchdb \n\n#### setup\n```python\n'''\nA class to handle reading and writing configuration data from couchdb\n\ninstantiate CouchConfig:\n        parameters:\n            uri: str\n'''\n\n# this is url for couchdb where are configuration data \nURI = 'http://tangledhub:tangledhub@couchdb-test:5984/thconfig-test/test_couch_config'\n\n# create intance CouchConfig and set URI property\nconfig = CouchConfig(URI)\n```\n\n#### fetch\nFetching configuration document from couchdb\n```python\n'''\nFetching document and store data in self._state\nSync couchdb -> self._state\nhttps://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid\n\nFetch:\n    parameters:\n        self: CouchConfig\n'''\n\n# this is url for couchdb where are configuration data \nURI = 'http://tangledhub:tangledhub@couchdb-test:5984/thconfig-test/test_couch_config'\n\n# create intance CouchConfig and set URI property\nconfig = CouchConfig(URI)\n\n# fetching data from database\nfetched_data = (await config.fetch()).unwrap()\n```\n\n#### commit\nCommit changes in configuration data in documment in couchdb\n```python\n'''\nCommit document, save data from self._state to couchdb\nSync self._state -> couchdb\nhttps://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid\n\nCommit:\n    parameters:\n        self: CouchConfig\n'''\n\n# this is url for couchdb where are configuration data \nURI = 'http://tangledhub:tangledhub@couchdb-test:5984/thconfig-test/test_couch_config_commit_changes'\n\n# create intance CouchConfig and set URI property\nconfig = CouchConfig(URI)\n\ntitle = 'Couch Config Example'\ndatabase = {'server': '192.168.1.1'}\n\n# set title and database\nconfig['title'] = title\nconfig['database'] = database\n\n# commit\ncommit_0 = (await config.commit()).unwrap()\n```\n\n### EtcdConfig \nConfiguration from EtcdConfig \n\n#### setup\n```python\n'''\nA class to handle reading and writing configuration data from etcd\ninstantiate EtcdConfig:\n    parameters:\n        HOST: str\n        PORT: int\n'''\n\n# you need to provide host and port\nHOST = 'etcd-test'\nPORT = 2379\n\n# create instance of EtcdConfig\nconfig = EtcdConfig(host = HOST, port = PORT)\n```\n\n#### fetch\nFetching configuration document from etcd\n```python\n'''\nFetching document and store data in self._state\nSync etcd -> self._state\nhttps://aetcd3.readthedocs.io/en/latest/reference/client.html#aetcd3.client.Etcd3Client.get_all\n\nFetch:\n    parameters:\n        self: EtcdConfig\n'''\n\n# you need to provide host and port\nHOST = 'etcd-test'\nPORT = 2379\n\n# create instance of EtcdConfig\nconfig = EtcdConfig(host = HOST, port = PORT)\n\n# fetching data from etcd\nfetched_data = (await config.fetch()).unwrap()\n```\n\n#### commit\nCommit changes in configuration data to etcd\n```python\n'''\nCommit document, save data from self._state to etcd\nSync self._state -> etcd\nhttps://aetcd3.readthedocs.io/en/latest/reference/client.html#aetcd3.client.Etcd3Client.put\n\ncommit changes:\n    parameters:\n        self: EtcdConfig\n'''\n\n# you need to provide host and port\nHOST = 'etcd-test'\nPORT = 2379\n\n# create instance of EtcdConfig\nconfig = EtcdConfig(host = HOST, port = PORT)\n\ntitle = 'Couch Config Example'\ndatabase = {'server': '192.168.1.1'}\n\n# set title and database\nconfig['title'] = title\nconfig['database'] = database\n\n# commit\ncommit_0 = (await config.commit()).unwrap()\n```\n\n<!-- Links -->\n\n<!-- Badges -->\n[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg\n[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause\n[build-image]: https://img.shields.io/badge/build-success-brightgreen\n[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green\n\n[pypi-project-url]: https://pypi.org/project/thquickjs/\n[stable-ver-image]: https://img.shields.io/pypi/v/thquickjs?label=stable\n[python-ver-image]: https://img.shields.io/pypi/pyversions/thquickjs.svg?logo=python&logoColor=FBE072\n[status-image]: https://img.shields.io/pypi/status/thquickjs.svg\n\n\n",
    'author': 'TangledHub',
    'author_email': 'info@tangledgroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tangledlabs/thconfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viewser',
 'viewser.commands',
 'viewser.commands.config',
 'viewser.commands.documentation',
 'viewser.commands.help',
 'viewser.commands.logs',
 'viewser.commands.model',
 'viewser.commands.notebooks',
 'viewser.commands.queryset',
 'viewser.commands.queryset.models',
 'viewser.commands.system',
 'viewser.error_handling',
 'viewser.settings',
 'viewser.storage',
 'viewser.tui',
 'viewser.tui.formatting']

package_data = \
{'': ['*']}

install_requires = \
['PyMonad>=2.4.0,<3.0.0',
 'click>=8.0.1,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'crayons>=0.4.0,<0.5.0',
 'docker>=5.0.0,<6.0.0',
 'environs>=9.3.1,<10.0.0',
 'fitin>=0.2.0,<0.3.0',
 'pandas>=1.2.3,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'pyarrow>=6.0.1,<7.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'strconv>=0.4.2,<0.5.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'toolz>=0.11.1,<0.12.0',
 'views-schema>=2.3.0,<3.0.0',
 'views-storage>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['viewser = viewser.cli:viewser']}

setup_kwargs = {
    'name': 'viewser',
    'version': '5.13.0',
    'description': 'The Views 3 CLI tool',
    'long_description': "\n# viewser\n\nThis package contains many useful user operations that are used by the views 3\nteam. These operations include fetching and publishing data, finding\ndocumentation on both transforms and database structure, and more.\n\n\n## CLI\n\n`viewser` functionality is exposed via a CLI on your system after installation.\nAn overview of available commands can be seen by running `viewser --help`.\n\n## API\n\nIn addition to the CLI, viewser exposes many useful operations as functions\nthat can be used in scripts.\n\n## Configuration\n\nThe tool is configured using the `viewser config set KEY VALUE` and `viewser\nconfig load JSON` commands. The settings shown without defaults here, or with\ndefaults that don't make sense for the average user (`REMOTE_URL`) must be\nconfigured before use.\n\n|Setting                          |Description                                        |Default            |\n|---------------------------------|---------------------------------------------------|-------------------|\n|RETRY_FREQUENCY                  |General request retry frequency in seconds         |5                  |\n|QUERYSET_MAX_RETRIES             |How many times a queryset is queried before failing|500                |\n|LOG_LEVEL                        |Determines what logging messages are shown         |INFO               |\n|ERROR_DUMP_DIRECTORY             |Determines where error dumps are written to        |~/.views/dumps     |\n|REMOTE_URL                       |URL of a views 3 instance                          |http://0.0.0.0:4000|\n|MODEL_METADATA_DATABASE_HOSTNAME |Hostname of database for storing model metadata    |hermes             |\n|MODEL_METADATA_DATABASE_NAME     |DBname of database for storing model metadata      |forecasts3         |\n|MODEL_METADATA_DATABASE_USER     |Username for database for storing model metadata   |Inferred from cert |\n|MODEL_METADATA_DATABASE_SSLMODE  |SSLmode for database for storing model metadata    |required           |\n|MODEL_METADATA_DATABASE_PORT     |Port of database for storing model metadata        |5432               |\n|MODEL_METADATA_DATABASE_SCHEMA   |Schema of database for storing model metadata      |forecasts          |\n|MODEL_METADATA_DATABASE_TABLE    |Table of database for storing model metadata       |model              |\n|AZURE_BLOB_STORAGE_ACCOUNT_NAME  |Name of Azure blob storage account                 |                   |\n|AZURE_BLOB_STORAGE_ACCOUNT_KEY   |Access key of Azure blob storage account           |                   |\n",
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/prio-data/viewser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

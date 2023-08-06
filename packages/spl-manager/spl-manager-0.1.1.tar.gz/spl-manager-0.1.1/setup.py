# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spl_manager']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3,<2.0',
 'deepdiff>=5.7,<6.0',
 'docker>=5.0,<6.0',
 'dynaconf>=3.1,<4.0',
 'fire>=0.4,<0.5',
 'inquirerpy>=0.3,<0.4',
 'requests-toolbelt>=0.9,<0.10',
 'rich>=11.0,<12.0',
 'splunk-appinspect>=2.14,<3.0',
 'splunk-sdk>=1.6,<2.0']

entry_points = \
{'console_scripts': ['spl = spl_manager.__main__:main']}

setup_kwargs = {
    'name': 'spl-manager',
    'version': '0.1.1',
    'description': 'A helper for Splunk-related development, maintenance, or migration operations.',
    'long_description': '# Splunk Management Utility\n\n<div align="center" >🤝 Show your support - give a ⭐️ if you liked the tool | Share on\n<a target="_blank" href=\'https://twitter.com/intent/tweet?url=https%3A%2F%2Fgithub.com%2Fnextpart%2Fspl-manager\'><img src=\'https://img.shields.io/badge/Twitter-1DA1F2?logo=twitter&logoColor=white\'/></a>\n| Follow us on\n <a target="_blank" href=\'https://www.linkedin.com/company/69421851\'><img src=\'https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white\'/></a>\n</br></br></br>\n\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\n</br>\n</div>\n\nThis library is an abstraction for Splunk-related development, maintenance, or migration\noperations. It provides a single CLI or SDK to conveniently perform various operations\nsuch as managing a local development container, retrieving sample-data, building\napplications, comparing instances, managing knowledge objects and hopefully much more in\nthe future.\n\n## Motivation 🔥\n\nWhen I work with Splunk, my working directory is usually in the same layout. I work with\na mono-repository or a higher-level one with submodules, which contains several\napplications and configuration. This can look generalized like this:\n\n```\n<Development Repository>\n├── apps                          # Folder where to store applications\n│   └── Defender_TA_nxtp          # Generic custom Splunk app\n├── dist                          # Place for built packages and reports\n├── scripts\n├── config                        # Settings and secrets\n│   └── settings.yaml             # General purpose settings for this lib\n│   └── .secrets.yaml             # API settings for connections and secrets\n└── share                         # Custom splunkbase or builtin app content\n```\n\nWe have all found our ways and methods to develop applications on an instance and to\nconfigure and operate that instance to meet our needs and/or those of our customers. But\nwhat is usually rather painful is when we then need them on other instances as well. A\ngood example are test instances, which should be as close to production as possible.\nHowever, in the last few years that I have been dealing as a user with Splunk, some\nneeds for simplified handling and automation have emerged that I would like to address\nhere.\n\n### We want to ...\n\n- Spin up a local development container:\n\n  ```bash\n  spl docker start\n  ```\n\n- Put my local application(s) there for testing purposes:\n\n  ```bash\n  spl docker upload --app="Defender*"\n  ```\n\n- Get sample data for Eventgen:\n\n  ```bash\n  spl --src="onprem"  samples --path="./apps/SA-Eventgen" download --name="WinDefender"\n  ```\n\n- (De)activate streaming of event data.\n\n- Download apps from development container to local folder:\n\n  ```bash\n  spl docker download --app="Defender*"\n  ```\n\n- Run AppInspect, Packaging, etc.:\n\n  ```bash\n  spl apps --name="Defender_TA*" validate\n  ```\n\n- List various objects on an instance:\n\n  ```bash\n  spl manager --conn="onprem" users list\n  ```\n\n- Create or modify objects on an instance:\n\n  ```bash\n  spl manager --conn="onprem" roles update --name "investigator"\n  ```\n\n- Sync objects and their properties from one instance to another:\n  ```bash\n  spl --src="onprem" --dest="localhost" sync users --create --update\n  ```\n\nand probably much more, so pull requests are welcome!\n\n## Getting Started 🚀\n\nYou can download the package from the package feed via `pip install spl-manager` or\ninstall from source with [poetry](https://python-poetry.org/) after cloning the\nrepository.\n\nThen you can issue your first command to get the help page:\n\n```bash\npython -m spl -h\n```\n\nor `poetry run python -m spl -h`. Anyhow it\'s recommended to set the\n`alias spl="python -m spl` for easier handling.\n\nYou have to create a `config\\.secrets.yaml` file by using the\n`config\\template.secrets.yaml` file, which contains the credentials for the Development\nDocker-Container and Splunkbase.\n\n## Using the library 📚\n\nPlease note that, when using the library as an SDK you need to pass the\n`interactive=False` flag to not run into issues because in _interactive_ mode it asks\nfor user inputs via CLI methods.\n\n```python\nfrom spl import SplManager\n\nspl = SplManager(interactive=False)\n```\n\n## Using the CLI 🧑\u200d💻\n\nIf you wish to get more information about any command within `spl`, you can pass the\n`-h` parameter.\n\n### Top-level `spl` Options\n\n- `--interactive`: Wether or not to run in interactive mode.\n- `--src`: The name of the source connection provided in settings.\n- `--dest`: The name of the destination connection provided in settings.\n\n### Top-level `spl` Modules\n\n- `connections` provides you a list of connections available via configuration.\n\n- `docker` helps you to manage the local splunk container instance.\n\n- `apps` abstracts the handling of local application folders at a given `--path` and\n  helps with validation, packaging, vetting, etc.\n\n- `samples` are based on the configured queries for a `--conn` or `--src` and can\n  download results and store them automatically at a `--path` to use for _SA-Eventgen_.\n\n- `manager` acts as a direct `ConnectionAdapter` interface for the specified `--conn`\n  parameter.\n\n- `sync` will handle `manager`s for `--src` and `--dest` connections, enabling you to\n  compare, move and update between those instances.\n\n## 🔗 References\n\n- [Splunk Python SDK](https://docs.splunk.com/Documentation/PythonSDK)\n- [Python Docker SDK (low-level API)](https://docker-py.readthedocs.io)\n- [Python Rich Outputs](https://rich.readthedocs.io)\n- [InquirerPy User Inputs](https://inquirerpy.readthedocs.io/)\n- [Python Fire CLI](https://github.com/google/python-fire)\n- [DeepDiff](https://zepworks.com/deepdiff/current/)\n- [Cerberus Schema Validation](https://docs.python-cerberus.org/)\n- [Splunk AppInspect](https://dev.splunk.com/enterprise/reference/appinspect)\n- [Splunk Packaging Toolkit](https://dev.splunk.com/enterprise/reference/packagingtoolkit)\n- [Splunk Eventgen](http://splunk.github.io/eventgen/)\n\n## 🤩 Support\n\n[![Support via PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=UXNY3UEYKBJ7L) or send us some crypto:\n\n| Protocol            | Address                                         |\n| ------------------- | ----------------------------------------------- |\n| Ethereum            | `0xcFC6Bdb68FB219de754D01BcD34F8A339549C910`    |\n| Avalanche           | `X-avax1vlrw8m9af5p4kx2zxc4d5lqmgh8c86uduwprg6` |\n| Harmony             | `one18fcze47fll6662ggr760u9jm3rfz859jkv7vyw`    |\n| Binance Chain       | `bnb1q6zg3pnmclnfhy6vtldfd0az97l0ndayun2tzn`    |\n| Binance Smart Chain | `0x1CD0ca3eC911Fe9661905Dd500FBaCE245c7013f`    |\n| Solana              | `Eh35fdT6gdMHcsj3TrTMnNDSgvWAEMc11Zhz9R96F7aB`  |\n',
    'author': 'Nextpart Security Intelligence',
    'author_email': 'info@nextpart.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

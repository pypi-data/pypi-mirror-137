# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ggci']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0',
 'flexmock>=0.10.4,<0.11.0',
 'pyyaml>=5.4.1,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'tenacity>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'ggci',
    'version': '1.1.0',
    'description': 'GitLab Google Chat Integration',
    'long_description': "# Gitlab Google Chat Integration\n\nA Python Flask web application that forwards webhook requests\nfrom GitLab to Google Chat.\n\n![GGCI showcase](https://raw.githubusercontent.com/lukany/ggci/cb0886eb6594e36c5e56e54f00dbfdb71d3d8629/showcase.png)\n\n## Installation\n\n`ggci` is available as a Python package\non [PyPI](https://pypi.org/project/ggci).\nIt can be installed via standard package managers in Python, e.g. pip:\n\n```sh\npip install ggci\n```\n\n## Usage\n\n`ggci` provides a standard Flask application factory `create_app()`:\n\n```python\nfrom ggci import create_app\n\napp = create_app()\n```\n\nFor how to use this application factory refer to the official [Flask\ndocumentation](https://flask.palletsprojects.com/en/1.1.x/).\n\n## Configuration\n\nThere are several ways how `ggci` can be configured.\n\n### YAML config (default)\n\nBy default `create_app()` looks for a YAML configuration file specified\nby `GGCI_CONFIG` environment variable.\nExample config:\n\n```YAML\nggci_secret: xxxxxxx\n\nuser_mappings:  # OPTIONAL, used for mentions; key: GitLab ID, val: Google Chat ID\n  5894317: 120984893489384029908  # Gandalf\n  4985120: 109238409842809234892  # Chuck Norris\n```\n\n### Config Object\n\nAlternatively, `create_app()` also accepts optional argument `config` of type\n`ggci.Config`.\n\n```python\nfrom ggci import Config, create_app\n\nconfig = Config(\n    ggci_secret='xxxxxxx',\n    user_mappings={\n        5894317: 120984893489384029908,  # Gandalf\n        4985120: 109238409842809234892,  # Chuck Norris\n    },\n)\n\napp = create_app(config=config)\n```\n\n## Features\n\n### Merge Request Events Notifications\n\nNotifications for merge requests actions.\nAll notifications for one MR are posted to the same thread (identified\nby merge request ID).\nSupported actions:\n\n- *open*: includes link with title, event author, mentions of assignees\n  and description\n- *approved*: includes link and event author\n- *update of assigness*: includes link and mentions of current assignees\n- *merged*: includes link and action author\n- *closed*: includes link and action author\n- *reopened*: includes link and action author\n",
    'author': 'Jan Lukány',
    'author_email': 'lukany.jan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukany/ggci',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

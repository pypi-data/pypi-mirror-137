# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos',
 'minos.cli',
 'minos.cli.api',
 'minos.cli.deploying',
 'minos.cli.templating',
 'minos.cli.wizards']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.2,<2.0.0',
 'copier>=5.1.0,<6.0.0',
 'rich>=10.14.0,<11.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['minos = minos.cli:main']}

setup_kwargs = {
    'name': 'minos-cli',
    'version': '0.1.1',
    'description': 'Command Line Interface for the Minos framework',
    'long_description': '<p align="center">\n  <a href="http://minos.run" target="_blank"><img src="https://raw.githubusercontent.com/minos-framework/.github/main/images/logo.png" alt="Minos logo"></a>\n</p>\n\n# Minos CLI: Minos\' microservices up and running\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/minos-cli.svg?label=minos-cli)](https://pypi.org/project/minos-microservice-aggregate/)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/minos-framework/minos-cli/pages%20build%20and%20deployment?label=docs)](https://minos-framework.github.io/minos-cli)\n[![License](https://img.shields.io/github/license/minos-framework/minos-cli.svg)](https://github.com/minos-framework/minos-cli/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/minos-framework/minos-cli/coverage.svg?branch=main)](https://codecov.io/gh/minos-framework/minos-cli)\n[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-Ask%20a%20question-green)](https://stackoverflow.com/questions/tagged/minos)\n[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/minos-framework/community)\n\n## Summary\n\nMinos CLI is a command line tool that helps you create and deploy Minos\' microservices. Through its simple command\nstructure, you\'ll get your microservices up and running as fast as you\'ve coded your business logic.\n\n## Quickstart\n\nFirst, we need to create a project to host our microservices\n\n```shell\nminos new project sample_project\ncd sample_project/\n```\n\nWe need to set some services that our project needs\n\n```shell\nminos set database postgres\nminos set broker kafka\nminos set apigateway minos\nminos set discovery minos\n```\n\nOnce we\'ve gone through all of these steps, the project is ready to accept a new microservice!\n\n```shell\ncd microservices/\nminos new microservice foo\n```\n\nTime to start coding! Yes, already!\n\n## Documentation\n\nComing soon...\n\n## Source Code\n\nThe source code of this project is hosted at [GitHub Repository](https://github.com/minos-framework/minos-cli).\n\n## Getting Help\n\nFor usage questions, the best place to go to is [StackOverflow](https://stackoverflow.com/questions/tagged/minos).\n\n## Discussion and Development\n\nMost development discussions take place over the [GitHub Issues](https://github.com/minos-framework/minos-cli/issues)\n. In addition, a [Gitter channel](https://gitter.im/minos-framework/community) is available for development-related\nquestions.\n\n## How to contribute\n\nWe are looking forward to having your contributions. No matter whether it is a pull request with new features, or the\ncreation of an issue related to a bug you have found.\n\nPlease consider these guidelines before you submit any modification.\n\n### Create an issue\n\n1. If you happen to find a bug, please file a new issue filling the \'Bug report\' template.\n2. Set the appropriate labels, so we can categorise it easily.\n3. Wait for any core developer\'s feedback on it.\n\n### Submit a Pull Request\n\n1. Create an issue following the previous steps.\n2. Fork the project.\n3. Push your changes to a local branch.\n4. Run the tests!\n5. Submit a pull request from your fork\'s branch.\n\n## License\n\nThis project is distributed under the [MIT](https://raw.githubusercontent.com/minos-framework/minos-cli/main/LICENSE)\nlicense.\n',
    'author': 'Minos Framework Devs',
    'author_email': 'hey@minos.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.minos.run/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

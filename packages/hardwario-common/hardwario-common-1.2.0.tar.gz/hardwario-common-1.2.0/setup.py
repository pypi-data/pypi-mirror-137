# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hardwario', 'hardwario.common']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['hardwario = hardwario.common.cli:main']}

setup_kwargs = {
    'name': 'hardwario-common',
    'version': '1.2.0',
    'description': 'HARDWARIO Common',
    'long_description': '<a href="https://www.hardwario.com/"><img src="https://www.hardwario.com/ci/assets/hw-logo.svg" width="200" alt="HARDWARIO Logo" align="right"></a>\n\n# HARDWARIO Common\n\n[![Main](https://github.com/hardwario/py-hardwario-common/actions/workflows/main.yaml/badge.svg)](https://github.com/hardwario/py-hardwario-common/actions/workflows/main.yaml)\n[![Release](https://img.shields.io/github/release/hardwario/py-hardwario-common.svg)](https://github.com/hardwario/py-hardwario-common/releases)\n[![PyPI](https://img.shields.io/pypi/v/hardwario-common.svg)](https://pypi.org/project/hardwario-common/)\n[![License](https://img.shields.io/github/license/hardwario/py-hardwario-common.svg)](https://github.com/hardwario/py-hardwario-common/blob/master/LICENSE)\n[![Twitter](https://img.shields.io/twitter/follow/hardwario_en.svg?style=social&label=Follow)](https://twitter.com/hardwario_en)\n\nThis repository contains Python package [hardwario-common](https://pypi.org/project/hardwario-common/)\n\n\n## License\n\nThis project is licensed under the [MIT License](https://opensource.org/licenses/MIT/) - see the [LICENSE](LICENSE) file for details.\n\n---\n\nMade with &#x2764;&nbsp; by [**HARDWARIO s.r.o.**](https://www.hardwario.com/) in the heart of Europe.\n',
    'author': 'Karel Blavka',
    'author_email': 'karel.blavka@hardwario.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hardwario/py-hardwario-common',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['maison', 'maison.config_sources']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pydantic>=1.8.2,<2.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['maison = maison.__main__:main']}

setup_kwargs = {
    'name': 'maison',
    'version': '1.4.0',
    'description': 'Maison',
    'long_description': '# Maison\n\n[![Actions Status](https://github.com/dbatten5/maison/workflows/Tests/badge.svg)](https://github.com/dbatten5/maison/actions)\n[![Actions Status](https://github.com/dbatten5/maison/workflows/Release/badge.svg)](https://github.com/dbatten5/maison/actions)\n[![codecov](https://codecov.io/gh/dbatten5/maison/branch/main/graph/badge.svg?token=948J8ECAQT)](https://codecov.io/gh/dbatten5/maison)\n[![PyPI version](https://badge.fury.io/py/maison.svg)](https://badge.fury.io/py/maison)\n\nRead configuration settings from configuration files.\n\n## Motivation\n\nWhen developing a `python` application, e.g a command-line tool, it can be\nhelpful to allow the user to set their own configuration options to allow them\nto tailor the tool to their needs. These options are typically set in files in\nthe root of a project directory that uses the tool, for example in a\n`pyproject.toml` or an `{project_name}.ini` file.\n\n`maison` aims to provide a simple and flexible way to read and validate those\nconfiguration options so that they may be used in the application.\n\n### Features\n\n- Supports multiple config files and multiple config filetypes.\n- Optional merging of multiple configs.\n- Optional config validation with [pydantic](https://pydantic-docs.helpmanual.io/).\n- Caching of config files for quick access.\n- Fully tested and typed.\n\n## Installation\n\n```bash\npip install maison\n```\n\n## Usage\n\nSuppose the following `pyproject.toml` lives somewhere in a project directory:\n\n```toml\n[tool.acme]\nenable_useful_option = true\n```\n\n`maison` exposes a `ProjectConfig` class to retrieve values from config files\nlike so:\n\n```python\nfrom maison import ProjectConfig\n\nconfig = ProjectConfig(project_name="acme")\n\nif config.get_option("enable_useful_option"):\n    # include the useful option\n```\n\n## Help\n\nSee the [documentation](https://dbatten5.github.io/maison) for more details.\n\n## Licence\n\nMIT\n',
    'author': 'Dom Batten',
    'author_email': 'dominic.batten@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbatten5/maison',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

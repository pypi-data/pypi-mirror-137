# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pygcc']

package_data = \
{'': ['*'], 'pygcc': ['default_db/*']}

install_requires = \
['lxml>=4.5.0,<5.0.0',
 'matplotlib>=3.2,<4.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.0,<2.0',
 'scipy>=1.2,<2.0']

setup_kwargs = {
    'name': 'pygcc',
    'version': '1.0.1',
    'description': 'A tool for thermodynamic calculations and geochemical database generation',
    'long_description': '# `pygcc`\n\n<img src="_static/PyGCC_logo_vector.jpg" alt="pygcc Logo" width="40%" align="right">\n\nA tool for thermodynamic calculations and geochemical database generation\n\n[![pyGeochemCalc Documentation](https://readthedocs.org/projects/pygcc/badge/?version=latest)](https://pygcc.readthedocs.io/en/latest/?badge=latest)\n[![License: GNU General Public License v3.0](https://img.shields.io/badge/License-GNU%20General%20Public%20License%20v3.0-blue.svg?style=flat)](https://bitbucket.org/Tutolo-RTG/pygcc/src/master/LICENSE)\n\n\npyGeochemCalc (pygcc) is a python-based program for thermodynamic calculations and producing the \nGeochemist\'s Workbench (GWB), EQ3/6, TOUGHREACT, and PFLOTRAN thermodynamic database from \nambient to deep Earth temperature and pressure conditions\n\n\npygcc is developed for use in the geochemical community by providing a consolidated \nset of existing and newly implemented functions for calculating the thermodynamic properties \nof gas, aqueous, and mineral (including solid solutions and variable-formula clays) species, \nas well as reactions amongst these species, over a broad range of temperature and pressure \nconditions, but is also well suited to being modularly introduced into other modeling tools \nas desired. The documentation is continually evolving, and more examples and tutorials will gradually be added (feel free to\nrequest features or examples; see [Contributing](#contributing) below).\n\n## Installation\n\n[![PyPI](https://img.shields.io/pypi/v/pygcc.svg?style=flat)](https://pypi.org/project/pygcc/)\n[![Compatible Python Versions](https://img.shields.io/pypi/pyversions/pygcc.svg?style=flat)](https://pypi.python.org/pypi/pygcc/)\n\n```bash\n$ pip install pygcc\n```\n\n## Examples\n\nCheck out the documentation for galleries of examples [General Usage](https://pygcc.readthedocs.io/en/latest/Example_1.html), \n[Integration with GWB](https://pygcc.readthedocs.io/en/latest/Example_2.html) and [Integration with EQ3/6](https://pygcc.readthedocs.io/en/latest/Example_3.html). \nIf you would prefer to flip through notebooks on Bitbucket, these same examples can be found in the folder [`docs/`](https://bitbucket.org/Tutolo-RTG/pygcc/src/master/docs/).\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. \nBy contributing to this project, you agree to abide by its terms. For more information, see the [documentation](https://pygcc.readthedocs.io/), \nparticularly the [Contributing page](https://pygcc.readthedocs.io/en/latest/contributing.html) and \n[Code of Conduct](https://pygcc.readthedocs.io/en/latest/conduct.html). \n\n## License\n\n`pygcc` was created by Adedapo Awolayo and Benjamin Tutolo. It is licensed under the terms of the GNU General Public License v3.0 license.\n\n## Citation\n\nIf you use pygcc for your research, citation of the software would be appreciated. It helps to quantify the impact of \npygcc, and build the pygcc community. For information on citing pygcc, \n[see the relevant docs page](https://pygcc.readthedocs.io/en/latest/pygcc_overview.html#citation-and-contact-information-a-class-anchor-id-section-6-a)\n\n## Credits\n\n`pygcc` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Adedapo Awolayo and Benjamin Tutolo',
    'author_email': None,
    'maintainer': 'Adedapo Awolayo and Benjamin Tutolo',
    'maintainer_email': 'benjamin.tutolo@ucalgary.ca',
    'url': 'https://bitbucket.org/Tutolo-RTG/pygcc/src/master/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

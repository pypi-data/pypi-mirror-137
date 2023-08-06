# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyCrystallography',
 'easyCrystallography.Components',
 'easyCrystallography.Elements',
 'easyCrystallography.Structures',
 'easyCrystallography.Symmetry',
 'easyCrystallography.io']

package_data = \
{'': ['*'], 'easyCrystallography': ['Databases/*']}

install_requires = \
['easyScienceCore>=0.2.0']

setup_kwargs = {
    'name': 'easycrystallography',
    'version': '0.1.0',
    'description': 'Crystallography in easyScience',
    'long_description': '# [![License][50]][51] [![Release][32]][33] [![Downloads][70]][71] [![CI Build][20]][21] \n\n[![CodeFactor][83]][84] [![Lines of code][81]](<>) [![Total lines][80]](<>) [![Files][82]](<>)\n\n\n<img height="80"><img src="https://raw.githubusercontent.com/easyScience/easyCrystallography/develop/resources/images/ec_logo.svg" height="65">\n\n**easyCrystallography** is a library that can be used for the generation and manipulation of crystal structures.\n\n## Install\n\n**easyCrystallography** can be downloaded using pip:\n\n```pip install easyCrystallography```\n\nOr direct from the repository:\n\n```pip install https://github.com/easyScience/easyCrystallography```\n\n## Test\n\nAfter installation, launch the test suite:\n\n```python -m pytest```\n\n[//]: # (## Documentation)\n\n[//]: # ()\n[//]: # (Documentation can be found at:)\n\n[//]: # ()\n[//]: # ([https://easyScience.github.io/easyCore]&#40;https://easyScience.github.io/easyCore&#41;)\n\n## Contributing\nWe absolutely welcome contributions. **easyCore** is maintained by the ESS and on a volunteer basis and thus we need to foster a community that can support user questions and develop new features to make this software a useful tool for all users while encouraging every member of the community to share their ideas.\n\n## License\nWhile **easyCore** is under the BSD-3 license\n\n<!---CI Build Status--->\n\n[20]: https://github.com/easyScience/easyCrystallography/workflows/CI%20using%20pip/badge.svg\n\n[21]: https://github.com/easyScience/easyCrystallography/actions\n\n\n<!---Release--->\n\n[32]: https://img.shields.io/pypi/v/easyCrystallography.svg\n\n[33]: https://pypi.org/project/easyCrystallography\n\n\n<!---License--->\n\n[50]: https://img.shields.io/github/license/easyScience/easyCrystallography.svg\n\n[51]: https://github.com/easyScience/easyCrystallography/blob/master/LICENSE.md\n\n\n<!---Downloads--->\n\n[70]: https://img.shields.io/pypi/dm/easyCrystallography.svg\n\n[71]: https://pypi.org/project/easyCrystallography\n\n<!---Code statistics--->\n\n[80]: https://tokei.rs/b1/github/easyScience/easyCrystallography\n\n[81]: https://tokei.rs/b1/github/easyScience/easyCrystallography?category=code\n\n[82]: https://tokei.rs/b1/github/easyScience/easyCrystallography?category=files\n\n[83]: https://www.codefactor.io/repository/github/easyscience/easyCrystallography/badge\n\n[84]: https://www.codefactor.io/repository/github/easyscience/easyCrystallography\n',
    'author': 'Simon Ward',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/easyScience/easyCrystallography',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

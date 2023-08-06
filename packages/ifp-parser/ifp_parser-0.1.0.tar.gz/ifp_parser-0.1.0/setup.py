# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ifp_parser']

package_data = \
{'': ['*'], 'ifp_parser': ['grammars/*']}

install_requires = \
['lark>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['ifp_parse = ifp_parser.__main__:main']}

setup_kwargs = {
    'name': 'ifp-parser',
    'version': '0.1.0',
    'description': '',
    'long_description': '# IFP_PARSER\n\nUse grammar rules to parse International Flight Plan Messages as described by the FAA.\n\n## References\n\nFAA Form 7233-4 IFP Appendix A\n<https://www.faa.gov/air_traffic/publications/atpubs/fs_html/appendix_a.html>\n',
    'author': 'nicholas',
    'author_email': 'nicholas.dilmaghani@gmail.com',
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

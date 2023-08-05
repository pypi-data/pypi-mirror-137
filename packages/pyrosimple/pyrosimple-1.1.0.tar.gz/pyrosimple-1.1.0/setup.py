# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyrosimple',
 'pyrosimple.daemon',
 'pyrosimple.data.config',
 'pyrosimple.io',
 'pyrosimple.scripts',
 'pyrosimple.torrent',
 'pyrosimple.ui',
 'pyrosimple.util']

package_data = \
{'': ['*'],
 'pyrosimple': ['data/htdocs/*',
                'data/htdocs/css/*',
                'data/htdocs/img/*',
                'data/htdocs/js/*',
                'data/img/*',
                'data/screenlet/*',
                'data/screenlet/themes/blueish/*',
                'data/screenlet/themes/default/*'],
 'pyrosimple.data.config': ['color-schemes/*',
                            'rtorrent.d/*',
                            'templates/*',
                            'templates/conky/*']}

install_requires = \
['Tempita>=0.5.2,<0.6.0', 'bencode.py>=4.0.0,<5.0.0']

entry_points = \
{'console_scripts': ['chtor = pyrosimple.scripts.chtor:run',
                     'lstor = pyrosimple.scripts.lstor:run',
                     'mktor = pyrosimple.scripts.mktor:run',
                     'rtcontrol = pyrosimple.scripts.rtcontrol:run',
                     'rtxmlrpc = pyrosimple.scripts.rtxmlrpc:run']}

setup_kwargs = {
    'name': 'pyrosimple',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'kannibalox',
    'author_email': 'kannibalox@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.6,<4',
}


setup(**setup_kwargs)

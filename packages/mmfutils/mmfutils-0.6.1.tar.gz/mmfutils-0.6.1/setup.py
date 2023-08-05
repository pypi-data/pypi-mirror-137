# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mmfutils',
 'mmfutils.math',
 'mmfutils.math.bases',
 'mmfutils.math.bases.tests',
 'mmfutils.math.integrate',
 'mmfutils.math.integrate.tests',
 'mmfutils.math.tests',
 'mmfutils.performance',
 'mmfutils.plot',
 'mmfutils.solve',
 'mmfutils.solve.tests',
 'mmfutils.tests']

package_data = \
{'': ['*']}

install_requires = \
['husl>=4.0.3,<4.1.0', 'zope.interface>=5.4.0,<5.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'doc': ['Sphinx>=3.5.4,<3.6.0',
         'mmf-setup>=0.3.1,<0.4.0',
         'mock>=4.0.3,<4.1.0',
         'nbconvert>=6.0.7,<6.1.0',
         'sphinx-rtd-theme>=0.5.2,<0.6.0'],
 'doc:python_version >= "3.6" and python_version < "4.0"': ['numpy',
                                                            'matplotlib'],
 'doc:python_version >= "3.7" and python_version < "4.0"': ['numpy>=1.20.2,<1.21.0',
                                                            'matplotlib>=3.4.1,<3.5.0'],
 'fftw': ['pyFFTW>=0.12.0,<0.13.0'],
 'test': ['ipyparallel>=6.3.0,<6.4.0',
          'numexpr>=2.7.3,<2.8.0',
          'persist>=3.0,<4.0',
          'psutil>=5.8.0,<5.9.0',
          'pyFFTW>=0.12.0,<0.13.0',
          'pytest>=6.2.3,<6.3.0',
          'pytest-cov>=2.11.1,<2.12.0',
          'uncertainties>=3.1.5,<3.2.0',
          'poetry>=1.1.12,<1.2.0'],
 'test:python_version < "3.10"': ['numba>=0.53.1,<0.54.0'],
 'test:python_version >= "3.6" and python_version < "4.0"': ['matplotlib',
                                                             'scipy'],
 'test:python_version >= "3.7" and python_version < "3.10"': ['scipy>=1.7.3,<1.8.0'],
 'test:python_version >= "3.7" and python_version < "4.0"': ['matplotlib>=3.4.1,<3.5.0']}

setup_kwargs = {
    'name': 'mmfutils',
    'version': '0.6.1',
    'description': 'Small set of utilities: containers and interfaces.',
    'long_description': 'Small set of utilities: containers and interfaces.\n\nThis package provides some utilities that I tend to rely on during development. Since I\nuse these in many different projects, I turned this into a repository so that I can\neasily sync and keep track of updates. Once the intreface and contents become stable, it\nwill probably make sense to include these directly along with the original project so\nthat an additional dependency is not introduced.\n',
    'author': 'Michael McNeil Forbes',
    'author_email': 'michael.forbes+python@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://alum.mit.edu/www/mforbes/hg/forbes-group/mmfutils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)

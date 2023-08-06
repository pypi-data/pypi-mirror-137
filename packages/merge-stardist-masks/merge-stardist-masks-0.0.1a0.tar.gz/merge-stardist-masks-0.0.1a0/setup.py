# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['merge_stardist_masks']

package_data = \
{'': ['*']}

install_requires = \
['stardist>=0.7.3,<0.8.0']

setup_kwargs = {
    'name': 'merge-stardist-masks',
    'version': '0.0.1a0',
    'description': 'Merge Stardist Masks',
    'long_description': "Merge Stardist Masks\n====================\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/merge-stardist-masks.svg\n   :target: https://pypi.org/project/merge-stardist-masks/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/merge-stardist-masks.svg\n   :target: https://pypi.org/project/merge-stardist-masks/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/merge-stardist-masks\n   :target: https://pypi.org/project/merge-stardist-masks\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/merge-stardist-masks\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/merge-stardist-masks/latest.svg?label=Read%20the%20Docs\n   :target: https://merge-stardist-masks.readthedocs.io/\n   :alt: Read the documentation at https://merge-stardist-masks.readthedocs.io/\n.. |Tests| image:: https://github.com/gatoniel/merge-stardist-masks/workflows/Tests/badge.svg\n   :target: https://github.com/gatoniel/merge-stardist-masks/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/gatoniel/merge-stardist-masks/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/gatoniel/merge-stardist-masks\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* This new post-processing step allows to use `StarDist`_ segmentation on\n  non-star-convex objects.\n\n  * Instead of NMS, this post-processing naively merges masks together\n\n  * Masks whos center points lie within another mask are added to that mask\n\n* Works in 2D and 3D\n\n* In 2D, it works on big and winding objects\n\n\nRequirements\n------------\n\n* A `StarDist`_ installation.\n\n\nInstallation\n------------\n\nYou can install *Merge Stardist Masks* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install merge-stardist-masks\n\n\nUsage\n-----\n\nPlease see the EXAMPLE in `Usage <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Merge Stardist Masks* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/gatoniel/merge-stardist-masks/issues\n.. _pip: https://pip.pypa.io/\n.. _StarDist: https://github.com/stardist/stardist\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://merge-stardist-masks.readthedocs.io/en/latest/usage.html\n",
    'author': 'Niklas Netter',
    'author_email': 'niknett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gatoniel/merge-stardist-masks',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tw_complex']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'scikit-learn>=1.0.2,<2.0.0', 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'tw-complex',
    'version': '1.0.3',
    'description': 'Algorithms for TW',
    'long_description': '![GitHub](https://img.shields.io/github/license/rafsaf/tw-complex)\n![PyPI](https://img.shields.io/pypi/v/tw-complex)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tw-complex)\n\n# TW Complex\n\nRepo with algorithms to divide ally villages into front and back in TW.\n\nUnderneath it is a problem of dividing a set of 2D points **A** according to the `min_radius` and `max_radius` distances from a set of other 2D points **B**, which can be solved most simply by counting the distances from each point in the first set **A** to all points in the second set **B** one by one.\n\n- [Instalation](#instalation)\n- [Basic usage](#basic-usage)\n- [Examples](#examples-before---after)\n- [Running locally](#running-locally)\n\n# Instalation\n\n```bash\npip install tw_complex\n```\n\n# Basic usage\n\n```python\nfrom tw_complex import CDistBrute\nimport numpy as np\n\n# The code for Example 1 below\n\npoints1 = np.random.rand(10000, 2) + [2, 0]\npoints2 = np.random.rand(15000, 2)\nmin_radius = 1.4\nmax_radius = 2\n\nprecise_front, precise_back = CDistBrute(\n    ally_villages=points1,\n    enemy_villages=points2,\n    min_radius=min_radius,\n    max_radius=max_radius,\n).result()\n\n```\n\n# Examples (before -> after)\n\n### Example 1\n\n```bash\nAlly: 10000 points\nEnemy: 15000 points\nmin_radius: 1.4\nmax_radius: 2\n```\n\n![example1](https://raw.githubusercontent.com/rafsaf/tw-complex/main/images/Figure_1.png)\n\n### Example 2\n\n```bash\nAlly: 2500 points\nEnemy: 6000 points\nmin_radius: 4\nmax_radius: 10\n```\n\n![example2](https://raw.githubusercontent.com/rafsaf/tw-complex/main/images/Figure_2.png)\n\n### Example 3\n\n```bash\nAlly: 20000 points\nEnemy: 20000 points\nmin_radius: 20\nmax_radius: 60\n```\n\n![example3](https://raw.githubusercontent.com/rafsaf/tw-complex/main/images/Figure_3.png)\n\n### Example 4\n\n```bash\nAlly: 20000 points\nEnemy: 20000 points\nmin_radius: 10\nmax_radius: 120\n```\n\n![example4](https://raw.githubusercontent.com/rafsaf/tw-complex/main/images/Figure_4.png)\n\n# Running locally\n\nYou will need to have [poetry](https://python-poetry.org/) installed.\n\n```\ngit clone https://github.com/rafsaf/tw-complex.git\ncd tw-complex\npoetry install\n\n```\n\nCode lives in `tw-complex` folder, and you may also test algorithms running in main folder\n\n```\n# In main folder\n# eg. ~/Desktop/tw-complex\n\npytest\n```\n\nFor CDistAndKNN it looks like\n\n```python\n# tests/test_cdist.py\n\nfrom tw_complex import CDistAndKNN\nimport tests.utils as utils\n\n\ndef test_CDistAndKNN():\n    utils.run_all_tests(CDistAndKNN, "CDistAndKNN", _precision=0.8, draw=True)\n\n# Go with `draw=False` if you do not want to use pyplot to show diagrams\n```\n\nSome hardcoded tests are located in `tests/utils.py`, it uses brute force for calculating exact result, then compare it to given algorithm using basic maths. You can even compare it to brute force itself (eg. using diffrent `_precision`). For new test there should be another file in `tests/test_name_of_file_in_tw_complex_folder.py` with pretty much the same content as above.\n',
    'author': 'rafsaf',
    'author_email': 'rafal.safin12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rafsaf/tw-complex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

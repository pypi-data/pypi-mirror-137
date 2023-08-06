# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_isort']

package_data = \
{'': ['*']}

install_requires = \
['isort>=4.0', 'pytest>=5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'pytest11': ['isort = pytest_isort']}

setup_kwargs = {
    'name': 'pytest-isort',
    'version': '3.0.0',
    'description': 'py.test plugin to check import ordering using isort',
    'long_description': "py.test plugin to check import ordering using isort\n===================================================\n\n.. image:: https://img.shields.io/pypi/v/pytest-isort.svg\n   :target: https://pypi.python.org/pypi/pytest-isort\n   :alt: Latest Version\n\n.. image:: https://github.com/stephrdev/pytest-isort/workflows/Test/badge.svg?branch=master\n   :target: https://github.com/stephrdev/pytest-isort/actions?workflow=Test\n   :alt: CI Status\n\n\nSupport\n-------\n\nPython 3.6, 3.7, 3.8, 3.9 and 3.10. pytest>=5.\n\n\nUsage\n-----\n\ninstall using ``pip``::\n\n    pip install pytest-isort\n\nActivate isort checks when calling ``py.test``::\n\n    py.test --isort\n\nThis will execute an isort check against every ``.py`` file (if its not ignored).\n\n\nExample\n-------\n\nGiven you have some files with incorrect sorted imports::\n\n    # content of file1.py\n\n    import os\n    import sys\n    import random\n\n    # content of file2.py\n\n    import json\n    import sys\n    import os\n\nIf you run ``py.test`` and activate the isort plugin you'll se something like this::\n\n    $ py.test --isort\n    ========================= test session starts ==========================\n    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.6.4\n    plugins: isort\n    collected 2 items\n\n    file1.py F\n    file2.py F\n\n    =============================== FAILURES ===============================\n    _____________________________ isort-check ______________________________\n    ERROR: file1.py Imports are incorrectly sorted.\n\n     import os\n    +import random\n     import sys\n    -import random\n    _____________________________ isort-check ______________________________\n    ERROR: file2.py Imports are incorrectly sorted.\n\n     import json\n    +import os\n     import sys\n    -import os\n    ======================= 2 failed in 0.02 seconds =======================\n\nIf you can't change the import ordering for ``file2.py``, you have the option to\nexclude ``file2.py`` from isort checks.\n\nSimply add the ``isort_ignore`` setting to your ``py.test`` configuration file::\n\n    [pytest]\n    isort_ignore =\n        file2.py\n\nThen re-run the tests::\n\n    $ py.test --isort\n    ========================= test session starts ==========================\n    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.6.4\n    plugins: isort\n    collected 1 items\n\n    file1.py F\n\n    =============================== FAILURES ===============================\n    _____________________________ isort-check ______________________________\n    ERROR: file1.py Imports are incorrectly sorted.\n\n     import os\n    +import random\n     import sys\n    -import random\n    ======================= 1 failed in 0.02 seconds =======================\n\nAs you can see, ``file2.py`` is ignored and not checked. Now fix the\nimport ordering in ``file1.py`` and re-run the tests::\n\n    $ py.test --isort\n    ========================= test session starts ==========================\n    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.6.4\n    plugins: isort\n    collected 1 items\n\n    file1.py .\n\n    ======================= 1 passed in 0.01 seconds ======================\n\nEverything is properly again. Congratulations!\n\nIf you run your testsuite again and again, ``py.test`` will only check changed\nfiles to speed up. You see this by adding ``-rs`` to your ``py.test`` options::\n\n    $ py.test --isort -rs\n    ========================= test session starts ==========================\n    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.6.4\n    plugins: isort\n    collected 1 items\n\n    file1.py s\n    ======================= short test summary info ========================\n    SKIP [1] pytest_isort.py:145: file(s) previously passed isort checks\n\n    ====================== 1 skipped in 0.01 seconds ======================\n\n\nConfiguration\n-------------\n\nYou can exclude files from isort checks by using the ``isort_ignore``\nsetting in your ``py.test`` configuration file (e.g. ``pytest.ini``)::\n\n    # content of setup.cfg\n    [pytest]\n    isort_ignore =\n        docs/conf.py\n        *migrations/*.py\n\nThis will ignore the ``conf.py`` python file inside the ``docs`` folder and\nalso ignore any python file in ``migrations`` folders.\n\nIn addition, excluded files in isort's configuration will be ignored too.\n\n\nNotes\n-----\n\nYou can use ``isort`` to rewrite your python files and re-order the imports but\nthis is not part of this plugin.\n",
    'author': 'Stephan Jaekel',
    'author_email': 'steph@rdev.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephrdev/pytest-isort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['savestate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'savestate',
    'version': '0.1.0',
    'description': 'Persistent storage of arbitrary python objects',
    'long_description': "# SaveState\n\n[![Coverage Status][coverage-badge]][coverage]\n[![GitHub Workflow Status][status-badge]][status]\n[![PyPI][pypi-badge]][pypi]\n[![GitHub][licence-badge]][licence]\n[![GitHub Last Commit][repo-badge]][repo]\n[![GitHub Issues][issues-badge]][issues]\n[![Python Version][version-badge]][pypi]\n\n```shell\npip install savestate\n```\n\n---\n\n**Documentation**: [https://mrthearman.github.io/savestate/](https://mrthearman.github.io/savestate/)\n\n**Source Code**: [https://github.com/MrThearMan/savestate/](https://github.com/MrThearMan/savestate/)\n\n---\n\nSaveState is a cross-platform fast file storage for arbitrary python objects. \nIt's similar to python's builtin [shelve][shelve] module, but aims to be more\nperformant on Windows while being cross-platform compatible.\n\nSavestate is inspired by [semidbm2][semidbm2], with a more modern interface.\nmapping-like functions, a context manager, and support for \narbitrary python objects.\n\n### Implementation details:\n- Pure python\n- No requirements or dependencies\n- A dict-like interface (no unions)\n- Same, single file on Windows and Linux (unlike shelve)\n- Key and value integrity can be evaluated with a checksum, which will detect data corruption on key access.\n- Recovery from missing bytes at the end of the file, or small amounts of corrupted data in the middle\n- Both values AND keys put in savestate must support [pickling][pickling].\nNote the [security implications][security] of this!\n  - This means that you can use arbitrary objects as keys if they support pickle (unlike shelve)\n- All the keys of the savestate are kept in memory, which limits the savestate size (not a problem for most applications)\n- NOT Thread safe, so cannot be accessed by multiple processes\n- File is append-only, so the more non-read operations you do, the more the file size is going to balloon\n  - However, you can *compact* the savestate, usually on *savestate.close()*, which will replace the savestate with a new file with only the current non-deleted data.\n  This will impact performance a little, but not by much\n  \n### Performance:\n- About 50-60% of the performance of shelve with [gdbm][gdbm] (linux), \n  but >5000% compared to shelve with [dumbdbm][dumbdbm] (windows) (>20000% for deletes!)\n  - Performance is more favorable with large keys and values when compared to gdbm, \n    but gdbm is still faster on subsequent reads/writes thanks to its caching\n- A dbm-mode for about double the speed of regular mode, but only string-type keys and values\n  - This is about 25-30% of the performance of gdbm on its own.\n  - Note: Values will be returned in bytes form!\n  \n> Source code includes a benchmark that you can run to get more accurate performance on your specific machine.\n\n\n[shelve]: https://docs.python.org/3/library/shelve.html\n[semidbm2]: https://github.com/quora/semidbm2\n[pickling]: https://docs.python.org/3/library/pickle.html#module-pickle\n[security]: https://docs.python.org/3/library/pickle.html#module-pickle\n[gdbm]: https://docs.python.org/3/library/dbm.html#module-dbm.gnu\n[dumbdbm]: https://docs.python.org/3/library/dbm.html#module-dbm.dumb\n\n[coverage-badge]: https://coveralls.io/repos/github/MrThearMan/savestate/badge.svg?branch=main\n[status-badge]: https://img.shields.io/github/workflow/status/MrThearMan/savestate/Tests\n[pypi-badge]: https://img.shields.io/pypi/v/savestate\n[licence-badge]: https://img.shields.io/github/license/MrThearMan/savestate\n[repo-badge]: https://img.shields.io/github/last-commit/MrThearMan/savestate\n[issues-badge]: https://img.shields.io/github/issues-raw/MrThearMan/savestate\n[version-badge]: https://img.shields.io/pypi/pyversions/savestate\n\n[coverage]: https://coveralls.io/github/MrThearMan/savestate?branch=main\n[status]: https://github.com/MrThearMan/savestate/actions/workflows/main.yml\n[pypi]: https://pypi.org/project/savestate\n[licence]: https://github.com/MrThearMan/savestate/blob/main/LICENSE\n[repo]: https://github.com/MrThearMan/savestate/commits/main\n[issues]: https://github.com/MrThearMan/savestate/issues\n",
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mrthearman.github.io/savestate/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)

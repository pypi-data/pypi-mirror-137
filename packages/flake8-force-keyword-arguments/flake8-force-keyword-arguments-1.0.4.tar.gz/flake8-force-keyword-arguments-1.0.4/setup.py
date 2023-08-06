# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_force_keyword_arguments']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8', 'marisa-trie>=0.7.7,<0.8.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata', 'typing-extensions']}

entry_points = \
{'flake8.extension': ['FKA1 = flake8_force_keyword_arguments:Checker']}

setup_kwargs = {
    'name': 'flake8-force-keyword-arguments',
    'version': '1.0.4',
    'description': 'A flake8 extension that is looking for function calls and forces to use keyword arguments if there are more than X arguments',
    'long_description': "# flake8-force-keyword-arguments\n\n[![PyPI](https://img.shields.io/pypi/v/flake8-force-keyword-arguments?label=pypi&logo=pypi&style=flat-square)](https://pypi.org/project/flake8-force-keyword-arguments/)\n[![PyPI - Wheel](https://img.shields.io/pypi/wheel/flake8-force-keyword-arguments?style=flat-square&logo=pypi)](https://pypi.org/project/flake8-force-keyword-arguments/)\n[![Python Version](https://img.shields.io/pypi/pyversions/flake8-force-keyword-arguments.svg?style=flat-square&logo=python)](https://pypi.org/project/flake8-force-keyword-arguments/)\n[![PyPI - Implementation](https://img.shields.io/pypi/implementation/flake8-force-keyword-arguments?style=flat-square&logo=python)]((https://pypi.org/project/flake8-force-keyword-arguments/))\n![Codecov](https://img.shields.io/codecov/c/gh/isac322/flake8-force-keyword-arguments?style=flat-square&logo=codecov)\n![GitHub last commit (branch)](https://img.shields.io/github/last-commit/isac322/flake8-force-keyword-arguments/master?logo=github&style=flat-square)\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/isac322/flake8-force-keyword-arguments/CI/master?logo=github&style=flat-square)\n![Dependabot Status](https://flat.badgen.net/github/dependabot/isac322/flake8-force-keyword-arguments?icon=github)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)\n___\n\nA flake8 plugin that is looking for function calls and forces to use keyword arguments\nif there are more than X (default=2) arguments.\nAnd it can ignore positional only or variable arguments functions such as `setattr()` or `Logger.info()`.\nThe plugin inspects given modules (via `--kwargs-inspect-module`, `--kwargs-inspect-module-extend`)\nto get signature and to determine whether it is positional only or variable arguments function.\nThe inspection runs only once at the start of the flake8 command and remembers ignore list through runtime.\n\n\n## Installation\n\n```\npip install flake8-force-keyword-arguments\n```\n\n## Usage\n\nRun your `flake8` checker [as usual](http://flake8.pycqa.org/en/latest/user/invocation.html).\n\nExample:\n\n```bash\nflake8 your_module.py\n```\n\n## Option\n\n- `--kwargs-max-positional-arguments`: How many positional arguments are allowed (default: 2)\n- `--kwargs-ignore-function-pattern`: Ignore pattern list (default: ('^logger.(:?log|debug|info|warning|error|exception|critical)$', '__setattr__$', '__delattr__$', '__getattr__$'))\n- `--kwargs-ignore-function-pattern-extend`: Extend ignore pattern list.\n- `--kwargs-inspect-module`: Inspect module level constructor of classes or functions to gather positional only callables and ignore it on lint. Note that methods are not subject to inspection. (default: ('builtins',))\n- `--kwargs-inspect-module-extend`: Extend `--kwargs-inspect-module`\n- `--kwargs-inspect-qualifier-option {only_name,only_with_qualifier,both}`: For detected positional only callables by inspection, option to append the qualifier or not. e.g. In case builtins.setattr(), `both` will register `builtins.setattr` and `setattr` as positional only function. `only_name` will register `setattr` and `only_with_qualifier` will register `builtins.setattr`. (default: QualifierOption.BOTH)\n\n## Example\n\n### code: `test.py`\n\n```python\nfrom functools import partial\n\ndef one_argument(one):\n    pass\n\ndef two_arguments(one, two):\n    pass\n\ndef pos_only_arguments(one, two, three, /):  # python 3.8 or higher required\n    pass\n\ndef variable_arguments(*args):\n    pass\n\nvariadic = lambda *args: None\ncurried = partial(variadic, 1)\n\none_argument(1)\none_argument(one=1)\ntwo_arguments(1, 2)\ntwo_arguments(one=1, two=2)\npos_only_arguments(1, 2, 3)\nvariadic(1, 2, 3)\ncurried(2, 3)\n```\n\n### Command\n\n#### `flake8 test.py --select FKA1 --kwargs-inspect-module-extend test`\n\n```\ntest.py:20:1: FKA100 two_arguments's call uses 2 positional arguments, use keyword arguments.\n```\n\n#### `flake8 test.py --select FKA1 --kwargs-inspect-module-extend test --kwargs-ignore-function-pattern-extend ^two_arguments$`\n\nNo error\n\n#### `flake8 test.py --select FKA1`\n\n```\ntest.py:16:11: FKA100 partial's call uses 2 positional arguments, use keyword arguments.\ntest.py:20:1: FKA100 two_arguments's call uses 2 positional arguments, use keyword arguments.\ntest.py:22:1: FKA100 pos_only_arguments's call uses 3 positional arguments, use keyword arguments.\ntest.py:23:1: FKA100 variadic's call uses 3 positional arguments, use keyword arguments.\ntest.py:24:1: FKA100 curried's call uses 2 positional arguments, use keyword arguments.\n```\n\n## Limitation\n\nCurrently it only inspects given modules and can not inspect (static, class or normal) methods.\nBecause inspection carries import, it is not safe to inspect all possible packages.\nAnd method case, the plugin can inspect methods signature and also can determine whether it is positional only or not.\nBut it can not use the information on lint time.\nBecause python is a dynamic typed language and flake8 is basically a static analyzer.\nThat is, flake8 can not get type information of `logger.debug()`.\nSo even if I know that `logging.Logger::debug()` is a variadic function,\nI can not assure that `logger` is a instance of `Logger`.\n\n## Error codes\n\n| Error code |                     Description                                |\n|:----------:|:--------------------------------------------------------------:|\n|   FKA100    | XXX's call uses N positional arguments, use keyword arguments. |\n",
    'author': 'Viktor Chaptsev',
    'author_email': 'viktor@chaptsev.ru',
    'maintainer': 'Byeonghoon Yoo',
    'maintainer_email': 'bh322yoo@gmail.com',
    'url': 'https://github.com/isac322/flake8-force-keyword-arguments',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

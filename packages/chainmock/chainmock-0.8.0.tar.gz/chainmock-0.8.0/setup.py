# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chainmock']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.0.0', 'typing-extensions']

entry_points = \
{'pytest11': ['chainmock = chainmock._pytest_plugin']}

setup_kwargs = {
    'name': 'chainmock',
    'version': '0.8.0',
    'description': 'Mocking library for Python and Pytest',
    'long_description': '<h1 align="center">Chainmock</h1>\n\n<p align="center">\n<a href="https://pypi.org/project/chainmock/">\n  <img src="https://img.shields.io/pypi/v/chainmock" alt="pypi">\n</a>\n<a href="https://github.com/ollipa/chainmock/actions/workflows/ci.yml">\n  <img src="https://github.com/ollipa/chainmock/actions/workflows/ci.yml/badge.svg" alt="ci">\n</a>\n<a href="https://chainmock.readthedocs.io/">\n  <img src="https://img.shields.io/readthedocs/chainmock" alt="documentation">\n</a>\n<a href="./LICENSE">\n  <img src="https://img.shields.io/pypi/l/chainmock" alt="license">\n</a>\n</p>\n\n<hr>\n\nMocking library for Python and Pytest.\n\nChainmock is a wrapper for Python unittest unit testing library. It provides an\nalternative syntax to create mocks and assertions with some additional features\nto make testing faster and more straightforward. The syntax works especially\nwell with pytest fixtures.\n\n**Documentation**: https://chainmock.readthedocs.io/\n\n## Installation\n\nInstall with pip:\n\n```\npip install chainmock\n```\n\n## Features\n\nChainmock supports all the same features that Python standard library unittest\nsupports and adds some convenient extra functionality.\n\n- **Mocking**: Create _mocks_ and assert call counts and arguments or replace\n  return values.\n- **Spying**: _Spying_ proxies the calls to the original function or method.\n  With spying you can assert call counts and arguments without mocking.\n- **Stubs**: Easily create _stub_ objects that can be used in tests as fake data\n  or to replace real objects.\n- **Async support**: Chainmock supports mocking and spying _async_ functions and\n  methods. Most of the time it also recognizes automatically when async mocking\n  should be used so it is not any harder than mocking sync code.\n- **Fully type annotated**: The whole codebase is fully type annotated so\n  Chainmock works well with static analysis tools and editor autocomplete.\n- Works with **Python 3.8+ and PyPy3**.\n\n## Examples\n\nThe entrypoint to Chainmock is the `mocker` function. Import the `mocker`\nfunction as follows:\n\n```python\nfrom chainmock import mocker\n```\n\n### Mocking\n\nTo mock you just give the object that you want to mock to the `mocker` function.\nAfter this you can start mocking individual attributes and methods as follows:\n\n```python\n# Assert that a certain method has been called exactly once\nmocker(Teapot).mock("add_tea").called_once()\n\n# Provide a return value and assert that method has been called twice\nmocker(Teapot).mock("brew").return_value("mocked").called_twice()\n\n# Assert that a method has been called with specific arguments at most twice\nmocker(Teapot).mock("add_tea").all_calls_with("green").call_count_at_most(2)\n```\n\n### Spying\n\nSpying is not any harder than mocking. You just need to call the `spy` method\ninstead of the `mock` method. After spying a callable, it works just like before\nspying and you can start making assertions on it.\n\n```python\n# Assert that a certain method has been called at least once\nmocker(Teapot).spy("add_tea").called()\n\n# Check that a method has been called at most twice and has\n# at least one call with the given argument\nmocker(Teapot).spy("add_tea").any_call_with("green").call_count_at_most(2)\n```\n\n### Stubs\n\nTo create a stub object, just call `mocker` function without any arguments.\n\n```python\n# Create a stub with a method called "my_method"\nstub = mocker().mock("my_method").return_value("it works!").self()\nassert stub.my_method() == "it works!"\n\n# You can give keyword arguments to the mocker function to quickly set properties\nstub = mocker(my_property=10)\nassert stub.my_property == 10\n```\n\nFor more details and examples, see the documentation.\n\n## Similar projects\n\nIf chainmock is not what you need, check out also these cool projects:\n\n- [flexmock](https://github.com/flexmock/flexmock): Chainmock\'s API is heavily\n  inspired by flexmock. Flexmock doesn\'t use standard library unittest and it\n  has fully custom mocking implementation. Compared to flexmock, chainmock has\n  more familiar API if you have been using standard library unittest. Chainmock\n  also supports async mocking and partial argument matching.\n- [pytest-mock](https://github.com/pytest-dev/pytest-mock/): Similar to\n  chainmock, pytest-mock is a wrapper for standard library unittest. However,\n  pytest-mock doesn\'t provide any extra functionality and it exposes unittest\n  mocks directly to the user.\n\n## Contributing\n\nDo you like this project and want to help? If you need ideas, check out the open issues and feel free to open a new pull request. Bug reports and feature requests are also very welcome.\n',
    'author': 'Olli Paakkunainen',
    'author_email': 'olli@paakkunainen.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ollipa/chainmock',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

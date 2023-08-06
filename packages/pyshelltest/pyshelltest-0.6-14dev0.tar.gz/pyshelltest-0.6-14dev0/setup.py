# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyshelltest']

package_data = \
{'': ['*']}

install_requires = \
['attrs==19.2.0',
 'flake8>=4.0.1,<5.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=6.2.5,<7.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'pyshelltest',
    'version': '0.6-14dev0',
    'description': 'Generate test cases for shell scripts',
    'long_description': '# PyShellTest\n\n[![Build/Test](https://github.com/bnichs/pyshelltest/actions/workflows/python-test.yml/badge.svg)](https://github.com/bnichs/pyshelltest/actions/workflows/python-test.yml)\n\nGenerate python test cases for shell commands based on simple configuration. Allows you to seemlessly test commands that need to be run from a shell but within the python testing framework. \n\nWe all need to write more tests and including outside commands allows for more coverage. \nFor instance:\n* Add linkchecker to your integ runs for a django project\n* Ensure tools in `bin/` have a `--help` \n\n\n# Installation\n```bash\npip install pyshelltest\n```\n\n# Integration\nAdd this to you test files where you see fit: \n```python \ngenerator = PyShellTestGenerator.from_json("sample-config.json")\ngenerator = PyShellTestGenerator.from_toml("sample-config.toml")\ntest_class = generator.generate()\n```\n\nYou can then run your tests like you would normally and PyShellTest will generate tests based on your conifg.json\n```\npython -m pytest tests/\n```\n\n\n#  Configuration\nSee `sample-config/` as well as `tests/test-config.toml`\n\n## Toml config\nExample configuration for a command:\n```toml\n[[command]]\n name = "the-command-name"\n\n# The command to run\ncommand = ["path/to/script.sh"]\n\n# How long to wait before timing out\ntimeout = 30\n\n# Print the output of the ocmmand to stdout\nprint_output = true\n\n# Expect this in stdout, fail otherwise\nstdout_contains = "bar" \n  \n# Expect this in stderr, fail otherwise\nstderr_contains = "bar"\n\n    # Set this dict if you expect errors from the command\n    [command.error] \n    # Expect an error\n    expect = true\n    \n    # Expect an error with this class\n    error_class = "FileNotFoundError"\n```\n\n\n## Json config\nExample configuration for a command: \n```json\n{\n    "command": [\n         {\n            "_comment":  "# The command name",\n            "name": "the-command-name",\n            \n            "_comment":  "# The command to run",\n            "command": ["path/to/script.sh"], \n            \n            "_comment":  "# How long to wait before timing out",\n            "timeout": 30, \n            \n            "_comment":  "# Print the output of the command to stdout",\n            "print_output": true,\n            \n            "_comment":  "# Expect this in stdout, fail otherwise",\n            "stdout_contains": "bar" ,\n              \n            "_comment":  "# Expect this in stderr, fail otherwise",\n            "stderr_contains": "bar",\n            \n            "_comment":  "# Set this dict if you expect errors from the command",\n            "error": { \n                "_comment":  "# Expect an error",\n                "expect": true,\n                \n                "_comment":  "# Expect an error with this class",\n                "error_class": "FileNotFoundError"\n            }\n        }\n    ]\n}\n```\n\n\n# Development \n\n## Testing\nHow to test this project\n\n\n```bash\npoetry run python -m pytest \n```',
    'author': 'Ben',
    'author_email': 'bnichs55@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bnichs/pyshelltest.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

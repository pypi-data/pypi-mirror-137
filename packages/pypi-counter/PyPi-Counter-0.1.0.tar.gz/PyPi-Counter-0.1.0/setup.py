# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['py_counter']
install_requires = \
['libcst>=0.4.0,<0.5.0', 'rich>=10.9.0,<11.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['pypicount = src.command_line_interface:cli']}

setup_kwargs = {
    'name': 'pypi-counter',
    'version': '0.1.0',
    'description': 'A counting program used for different Pythong packages and modules.',
    'long_description': '# PyPiCount\n\n## Overview\n\n- This project is a tool that, on its own, will provide assistance to\ncomputer science professors to assist in grading assignments.\nThis tool will count and output the number of \'common errors\'\n(e.g., Classes without docstrings, functions without docstrings, etc.)\nas well as the number of common computing structures (e.g.,\nfunctions, Classes, looping constructs, imports, etc.)\nall as specified by the user in the command line interface.\n\n- This project also can serve as a collaborative enhancement\nto import this tool into Allegheny College\'s\nown GatorGrader to create new GatorGrader checks.\nThe program utilizes LibCST, which parses Python\ncode as a CST (Concrete Syntax Tree)\nthat keeps all formatting details (comments,\nwhite spaces, parentheses, etc.).\nAs a released tool on PiPy, this tool can be imported into\nany other automated grading tool as well.\n\n## Usefulness of Project\n\n- Within LibCST, it has many nodes to "match" modules, expressions, and\nstatements which allowed us as programmers to complete our user stories in a\nmore uniform way. This project is useful because of the exploration of LibCST,\nwhich ultimately allows end users to specify a given construct they would like\nto identify in the source code (as LibCST will find all matches of this construct).\n\n## Getting Started\n\nUsers can get started with this project by following the following steps:\n\n1. Clone this repository and `cd` into the project folder\n2. Run the command ```poetry install``` to install the dependencies for this project.\n3. To familiarize yourself with the arguments accepted for this project, run the\ncommand ```poetry run pypicount --help```. This command displays all of the\ndifferent arguments that can be passed. The list of the different arguments\nare listed below:\n\n  ```python\n  Options:\n    --input-file PATH              [required]\n    --class_def                    [default: False]\n    --import_statements            [default: False]\n    --comment                      [default: False]\n    --function_def                 [default: False]\n    --if_statements                [default: False]\n    --function_without_docstrings  [default: False]\n    --function_with_docstrings     [default: False]\n    --class_with_docstrings        [default: False]\n    --class_without_docstrings     [default: False]\n    --install-completion           Install completion for the current shell.\n    --show-completion              Show completion for the current shell, to\n                                   copy it or customize the installation.\n\n    --help                         Show this message and exit.\n\n  ```\n\nThese are the different types of arguments that PyPiCount will accept in this release.\n\nOnce you find your chosen arguments, run the following:\n\n```python\npoetry run pypicount --[argument] --input-file path/to/file\n```\n\n## Example of Output\n\nSample run command:\n\n```python\npoetry run pypicount --class_with_docstrings --input-file tests/input/sample_file.py\n```\n\nSample Output:\n\n```python\n# of functions with docstrings: 1\n\n## Help and Bug Fixes\n\n- Users who are having trouble with navigating the program can come to the ReadMe\nfor assistance.\n- Users can also open an issue on our [Issue Tracker](https://github.com/cmpsc-481-s22-m1/PyCount/issues)\nwith the following format:\n  - Describe the bug\n  - Include steps to replicate the bug\n  - Expected behavior\n  - Screenshots\n  - Desktop OS\n\n## Authors\n\n- The people who maintain and contribute to this project are\n  - Alexis Caldwell, [@caldwella2](https://github.com/caldwella2)\n  - Adriana Solis, [@solisa986](https://github.com/solisa986)\n  - Rachael Harris, [@rachaelharris](https://github.com/rachaelharris)\n  - Ramon Guzman, [@guzmanr04](https://github.com/guzmanr04)\n  - Ryan Hilty, [@RyanHiltyAllegheny](https://github.com/RyanHiltyAllegheny)\n',
    'author': 'Adriana Solis, Alexis Caldwell, Rachael Harris, Ramon Guzman, Ryan Hilty',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cmpsc-481-s22-m1/PyPiCounter/tree/main',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

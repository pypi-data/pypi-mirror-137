# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylocalc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylocalc',
    'version': '0.5.2',
    'description': 'Python interface for manipulating LibreOffice Calc spreadsheets',
    'long_description': '# This project is no longer maintained!\n\n> Sorry...\n\n# PyLOcalc\n\n[![forthebadge](https://forthebadge.com/images/badges/0-percent-optimized.svg)](https://forthebadge.com)\n[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)\n[![forthebadge](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com)\n\nPython interface for manipulating LibreOffice Calc spreadsheets\n\n**DISCLAIMER: This is not production software! Backup your document before trying it!**\n\n## About\n\nLibreOffice/OpenOffice has API for many languages including Python, thanks to the Universal Network Objects (UNO).\n\n_But its API is all but [Pythonic](https://docs.python.org/3/glossary.html)!_\n\nI took inspiration from [this article](https://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html)\nand created simple wrapper around this API.\n\nPyLOcalc also automatically opens a headless LibreOffice Calc document with basic read, write, and save functionality.\nTherefore, it can be used as a library for other scripts that manipulate spreadsheets.\n\n## Requirements\n\n1. **python>=3.8**\n2. You have to have LibreOffice with "python support" installed.\n   In Ubuntu it\'s (apparently) `sudo apt install libreoffice-script-provider-python`,\n   in Arch Linux I didn\'t have to do anything.\n\n   You can try running `python -m uno` and it should not produce any output or error.\n3. Macro security - Medium. Follow [this article](https://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html).\n\n## Installation\n\n```bash\npip install pylocalc\n```\n\n## Basic usage\n\n```python\nimport pylocalc\n\ndoc = pylocalc.Document(\'path/to/calc/spreadsheet.ods\')\n# You have to connect first\ndoc.connect()\n\n# Get the sheet by index\nsheet = doc[2]\n# Or by name\nsheet = doc[doc.sheet_names[1]]\n\n# Get the cell by index\ncell = sheet[10, 14]\n# Or by "name"\ncell = sheet[\'B12\']\n\n# Read and set cell value\nprint(cell.value)\n> \'Some value\'\n\ncell.value = 12.2\nprint(cell.value)\n> \'12.2\'\n\ncell.value = \'Other value\'\nprint(cell.value)\n> \'Other value\'\n\n# Don\'t forget to save and close the document!\ndoc.save()\ndoc.close()\n```\n\n## Append rows and columns\n\nPyLOcalc can append row and column values to the first available row or column.\nIt looks at the cell at the `offset` (default 0) and if the cell is empty it adds values there.\n\n```python\nimport decimal\nimport pylocalc\n\ndoc = pylocalc.Document(\'path/to/calc/spreadsheet.ods\')\ndoc.connect()\nsheet = doc[\'Totals\']\n\nsheet.append_row((\'2021-01-01\', 123, 12.3, decimal.Decimal("0.111"), \'Yaaay\'), offset=1)\n\nsheet.append_column((\'New column header\'))\n\ndoc.save()\ndoc.close()\n```\n\n## Context manager\n\nPyLOcalc `Document` can be used as context manager that automatically connects and closes the document.\nIf no error is raised in the context block it also **saves the document**.\n\n```python\nimport pylocalc\nwith pylocalc.Document(\'path/to/calc/spreadsheet.ods\') as doc:\n    doc[0][1,10].value = \'I ❤️ context managers\'\n```\n',
    'author': 'Viliam Valent',
    'author_email': 'pylocalc@viliamvalent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ViliamV/pylocalc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

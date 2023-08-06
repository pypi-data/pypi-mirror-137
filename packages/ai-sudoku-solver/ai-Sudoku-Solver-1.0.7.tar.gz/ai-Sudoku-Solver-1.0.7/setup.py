# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ai_sudoku_solver']

package_data = \
{'': ['*']}

install_requires = \
['huggingface-hub==0.2.1', 'numpy==1.20.1', 'tensorflow==2.7.0', 'tqdm==4.59.0']

setup_kwargs = {
    'name': 'ai-sudoku-solver',
    'version': '1.0.7',
    'description': 'A python library for solving sudoku puzzles using artificial neural networks',
    'long_description': '# [ai-Sudoku-Solver](https://github.com/Ritvik19/ai-Sudoku-Solver)\n\nSolving Sudoku Puzzles using Artificial Neural Networks\n\n[![Downloads](https://pepy.tech/badge/ai-sudoku-solver)](https://pepy.tech/project/ai-sudoku-solver)\n[![Downloads](https://pepy.tech/badge/ai-sudoku-solver/month)](https://pepy.tech/project/ai-sudoku-solver)\n[![Downloads](https://pepy.tech/badge/ai-sudoku-solver/week)](https://pepy.tech/project/ai-sudoku-solver)\n\n---\n\n## Table of Contents\n\n- [ai-Sudoku-Solver](#ai-sudoku-solver)\n  - [Table of Contents](#table-of-contents)\n  - [Installation](#installation)\n  - [Usage](#usage)\n  - [Model Gallery](#model-gallery)\n  - [References](#references)\n\n---\n\n## Installation\n\n```bash\npip install ai-sudoku-solver\n```\n\n---\n\n## Usage\n\nInstantiate a SudokuSolver object\n\n```python\nfrom ai_sudoku_solver import SudokuSolver\n\nsolver = SudokuSolver("Ritvik19/sudoku-net-v1")\n```\n\nCall the model on your puzzles\n\n```python\npuzzle = np.array([[\n    [0, 0, 4, 3, 0, 0, 2, 0, 9],\n    [0, 0, 5, 0, 0, 9, 0, 0, 1],\n    [0, 7, 0, 0, 6, 0, 0, 4, 3],\n    [0, 0, 6, 0, 0, 2, 0, 8, 7],\n    [1, 9, 0, 0, 0, 7, 4, 0, 0],\n    [0, 5, 0, 0, 8, 3, 0, 0, 0],\n    [6, 0, 0, 0, 0, 0, 1, 0, 5],\n    [0, 0, 3, 5, 0, 8, 6, 9, 0],\n    [0, 4, 2, 9, 1, 0, 3, 0, 0]\n]])\nsolution = solver(puzzle)\n# array([[\n#     [8, 6, 4, 3, 7, 1, 2, 5, 9],\n#     [3, 2, 5, 8, 4, 9, 7, 6, 1],\n#     [9, 7, 1, 2, 6, 5, 8, 4, 3],\n#     [4, 3, 6, 1, 9, 2, 5, 8, 7],\n#     [1, 9, 8, 6, 5, 7, 4, 3, 2],\n#     [2, 5, 7, 4, 8, 3, 9, 1, 6],\n#     [6, 8, 9, 7, 3, 4, 1, 2, 5],\n#     [7, 1, 3, 5, 2, 8, 6, 9, 4],\n#     [5, 4, 2, 9, 1, 6, 3, 7, 8]\n# ]])\n```\n\n---\n\n## Model Gallery\n\n| model                                                          | # parameters |  trained on | accuracy |\n| -------------------------------------------------------------- | -----------: | ----------: | -------: |\n| [sudoku-net-v1](https://huggingface.co/Ritvik19/sudoku-net-v1) |    3,784,729 |  1M puzzles |   98.138 |\n| [sudoku-net-v2](https://huggingface.co/Ritvik19/sudoku-net-v2) |    3,784,729 | 10M puzzles |   98.212 |\n\n## References\n\n1. [1 million Sudoku games](https://www.kaggle.com/bryanpark/sudoku)\n2. [9 Million Sudoku Puzzles and Solutions](https://www.kaggle.com/rohanrao/sudoku)\n',
    'author': 'Ritvik19',
    'author_email': 'rastogiritvik99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

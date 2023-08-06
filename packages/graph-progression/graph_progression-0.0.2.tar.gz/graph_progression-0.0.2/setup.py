# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graph_progression']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'graph-progression',
    'version': '0.0.2',
    'description': 'Create a progression of recommendations from a user-supplied recommender',
    'long_description': '# Progression\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nCreate a progression of recommendations from a user-supplied recommender. For more info, see our [official docs](https://askarthur.github.io/graph-progression)\n\n## General\n\nThis package was made for a specific use-case but should work with any *content-based* recommendation engine and possibly user-based recommenders.\n\nThe initial use case was to create a visual progression of artwork recommendations. This was done to create interesting collections of fine artworks powered by our computer vision recommendation engine.\n\nTo see an example, see our [samples](docs/samples/README.md).\n\n## Quickstart\n\n### Install\n\n`pip install graph-progression`\n\n### Implement\nProgession has a full sample set to show the functionality of the package w/o the need of a recommender.\n\n```python\nfrom graph_progression import DFSProgressor, random_walk\n\nprogressor = DFSProgressor()\nprogressor.create_progression(0, random_walk, progression_length=3)  \n# [0, 8114, 9353]\n\nprogressor.graph\n# {\n# 0: [8114, 5298, 2050, 4837, 1376, 2924, 8689, 8000, 2171, 3246], \n# 8114: [9353, 8647, 8768, 8391, 8555, 8879, 9102, 9481, 9282, 8142]\n# }\n```\n\nAs you can see, progession generates "recommendations" at each step, uses them to populate a graph (for memoization), and then continues on. Not shown here, but it also has the intelligence to backtrack using the graph if it ends a recommendation (node) with no recommedations (edges).\n\n## Features\n\n- Recommendation progression via sequential depth-first search\n- Memoization\n- Flexible API that can take as inputs:\n  - Starter graph\n  - Recommendation algorithm\n  - Post recommendation filters\n  - Selection algorithm\n  - Progession length\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`mgancita/cookiecutter-pypackage`](https://mgancita.github.io/cookiecutter-pypackage/) project template.\n',
    'author': 'Marco Gancitano',
    'author_email': 'marco.gancitano@askarthur.art',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/askarthur/graph-progression',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routor', 'routor.api', 'routor.utils']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'fastapi',
 'more-itertools>8.0.0',
 'networkx-astar-path>=1.0.1',
 'networkx>2.5',
 'osmnx>1.1.0',
 'pydantic>1.5.0',
 'python-dotenv>0.15.0',
 'scikit-learn',
 'uvicorn']

entry_points = \
{'console_scripts': ['routor = routor.cli:main']}

setup_kwargs = {
    'name': 'routor',
    'version': '0.7.1',
    'description': 'Simple osm routing engine.',
    'long_description': '# routor\n\n![PyPI](https://img.shields.io/pypi/v/routor?style=flat-square)\n![GitHub Workflow Status (main)](https://img.shields.io/github/workflow/status/escaped/routor/Test%20&%20Lint/main?style=flat-square)\n![Coveralls github branch](https://img.shields.io/coveralls/github/escaped/routor/main?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/routor?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/routor?style=flat-square)\n\nSimple routing engine for OpenStreetMaps with easy to customize profiles/weight-functions. \n\n## Requirements\n\n* Python 3.6.1 or newer\n\n## Installation\n\n```sh\npip install routor\n```\n\n## Usage\n\n### CLI\n\nThe CLI offers multiple commands, use `routor --help` to find out more.\n\n#### Download map\n\nDownloads a compatible map from OSM, eg.\n\n```sh\nroutor download "Bristol, England" ./bristol.graphml\n```\n\nBy default it only adds a handful of tags ([nodes](https://github.com/gboeing/osmnx/blob/77b2535776b4397ae0deda402398609b3a4694a6/osmnx/settings.py#L5), [edge](https://github.com/gboeing/osmnx/blob/77b2535776b4397ae0deda402398609b3a4694a6/osmnx/settings.py#L49)) to the graph.\nUse `-n` or `-e` to add other available tags ([edge](https://github.com/gboeing/osmnx/blob/77b2535776b4397ae0deda402398609b3a4694a6/osmnx/settings.py#L29), [node](https://github.com/gboeing/osmnx/blob/77b2535776b4397ae0deda402398609b3a4694a6/osmnx/settings.py#L28)) as well.\nAdditionally, you can download multiple regions at once:\n\n```sh\nroutor download -n junction -n traffic_signals -e surface -e lanes "Bristol, England" "Somerset, England" ./bristol_somerset.graphml\n```\n\nBy default, each downloaded map is enhanced with\n\n* `street_count` - how many physical segments are connected to a node\n* `bearing` - angle of each edge\n* `speed_kph` - free-flow travel speed based on `maxspeed`, fallback is set to `30` kph (see [osmnx](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.speed.add_edge_speeds) for more information)\n* `travel_time` - Travel time based on `speed_kph` and `length`\n\nIf you provide a [Google API](https://developers.google.com/maps/documentation/javascript/get-api-key) (using --api-key), the following additional attributes are available:\n\n* `elevation` - elevation above sea level\n* `grade`/`grade_abs` - grade of an endge\n\n#### Calculate route\n\nDetermine the optimal route between two points using the given weight function and print the route as `JSON` to `stdout`.\n\n```sh\nroutor route -- ./bristol.graphml  "51.47967237816338,-2.6174926757812496" "51.45422084861252,-2.564105987548828" "routor.weights.length"\n```\n\n### Web API\n\n#### Configuration\n\nThe configuration is either read from a `.env` file or the environment.\nBefore you are able to run the server, you have to set the variables mentioned in [routor/api/config.py](routor/api/config.py).\n\n#### Run the API\n\nThe api is served using [uvicorn](https://www.uvicorn.org/).\nTo start the server run\n\n```sh\nuvicorn routor.api.main:app\n```\n\nThe API will be available at http://127.0.0.1:8000 and the docs at http://127.0.0.1:8000/docs.\n\n### As library\n\nYou can also use the engine as a library.\nTo calculate a route from A to B you can do\n\n```python\nfrom pathlib import Path\n\nfrom routor.engine import Engine\nfrom routor import models, weights\n\n...\nmap_path = Path(...)\nengine = Engine(map_path)\n\norigin = models.Location(latitude=51.47967237816338, longitude=-2.6174926757812496)\ndestination = models.Location(latitude=51.45422084861252, longitude=-2.564105987548828)\n\nroute = engine.route(origin, destination, weight_func=weights.length, travel_time_func=weights.travel_time)  # shortest distance\n```\n\n## Available weight-functions\n\n### `"length"` / `routor.weights.length`\n\nCalculates the shortest path from A to B, only the length of an edge is taken into account.\n\n### `"travel_time"` / `routor.weight.travel_time`\n\nCalculates the fastest route based on [travel time](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.speed.add_edge_travel_times).\n\n## Plugins\n\n`routor` implements a simple plugin mechanism.\nSimply create a new module with the prefix `routor_`, make it available (install it, `sys.path` hack or similar) and it will be automatically discovered and loaded.\nDepending on how you structure your module/plugin, you have to do the registration of the additional functionality in either `routor_YOUR_MODULE/__init__.py` or `routor_YOUR_MODULE.py`.\n\n### Register a new weight function\n\nExisting weight functions are defined in [routor/weights.py](routor/weights.py) and can be taken as reference.\nTo register a new function in your plugin, you have to implement something similar to\n\n```python\n# __init__.py\nfrom typing import Optional\n\nfrom routor.weights import register\nfrom routor import models\n\n\ndef my_weight_func(prev_edge: Optional[models.Edge], edge: models.Edge) -> float:\n    ...\n    return ...\n\n\nregister(my_weight_func, "weight_func")\n```\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for packaging and\nmanaging all dependencies and [pre-commit](https://pre-commit.com/) to run\n[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),\n[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).\n\nAdditionally, [pdbpp](https://github.com/pdbpp/pdbpp) and [better-exceptions](https://github.com/qix-/better-exceptions) are installed to provide a better debugging experience.\nTo enable `better-exceptions` you have to run `export BETTER_EXCEPTIONS=1` in your current session/terminal.\n\nClone this repository and run\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n\nto create a virtual enviroment containing all dependencies.\nAfterwards, You can run the test suite using\n\n```bash\npoetry run pytest\n```\n\nThis repository follows the [Conventional Commits](https://www.conventionalcommits.org/)\nstyle.\n\n### Cookiecutter template\n\nThis project was created using [cruft](https://github.com/cruft/cruft) and the\n[cookiecutter-pyproject](https://github.com/escaped/cookiecutter-pypackage) template.\nIn order to update this repository to the latest template version run\n\n```sh\ncruft update\n```\n\nin the root of this repository.\n',
    'author': 'Alexander Frenzel',
    'author_email': 'alex@relatedworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/escaped/routor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['airpyllution']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.3,<5.0',
 'altair-viewer>=0.4.0,<0.5.0',
 'altair>=4.2.0,<5.0.0',
 'black>=21.12b0,<22.0',
 'mock>=4.0.3,<5.0.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'plotly>=5.5.0,<6.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.27.1,<3.0.0',
 'responses>=0.17.0,<0.18.0',
 'vega-datasets>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'airpyllution',
    'version': '2.0.1',
    'description': 'A package which  provides various functionalities on air pollution data.',
    'long_description': '# airpyllution\n[![codecov](https://codecov.io/gh/UBC-MDS/airpyllution/branch/main/graph/badge.svg?token=c6vEGpbs3h)](https://codecov.io/gh/UBC-MDS/airpyllution)\n[![build](https://github.com/UBC-MDS/airpyllution/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/airpyllution/actions/workflows/build.yml)\n[![deploy](https://github.com/UBC-MDS/airpyllution/actions/workflows/deploy.yml/badge.svg)](https://github.com/UBC-MDS/airpyllution/actions/workflows/deploy.yml)\n\n`airpyllution` is a Python package for visualizing or obtaining future, historic and current air pollution data using the [OpenWeather API](https://openweathermap.org). Our goal is to enable users the ability to explore air pollution levels in locations around the world by providing visual charts and graphs. We make the data accessible and easy to comprehend in just a few lines of code.\n\nAlthough there is an abundance of python weather packages and APIs in the Python ecosystem (e.g. [python-weather](https://pypi.org/project/python-weather/), [weather-forecast](https://pypi.org/project/weather-forecast/)), this particular package looks at specifically air pollution data and uses the [Air Pollution API](https://openweathermap.org/api/air-pollution) from OpenWeather. This is a unique package which provides simple and easy to use functions and allows users to quickly access and visualise data.\n\nThe data returned from the API includes the polluting gases such as Carbon monoxide (CO), Nitrogen monoxide (NO), Nitrogen dioxide (NO2), Ozone (O3), Sulphur dioxide (SO2), Ammonia (NH3), and particulates (PM2.5 and PM10).\n\nUsing the OpenWeatherMap API requires sign up to gain access to an API key.   \nFor more information about API call limits and API care recommendations please visit the [OpenWeather how to start](https://openweathermap.org/appid) page.\n## Functions\nThis package contains 3 functions: \n- `get_air_pollution()`\n- `get_pollution_history()`\n- `get_pollution_forecast()`\n\n### `get_air_pollution()`\nFetches the air pollution levels based on a location. Based on the values of the polluting gases, this package uses the [Air Quality Index](https://en.wikipedia.org/wiki/Air_quality_index#CAQI) to determine the level of pollution for the location and produces a coloured map of the area displaying the varying regions of air quality.\n\n### `get_pollution_history()`\nRequires a start and end date and fetches historic air pollution data for a specific location. The function returns a data frame with the values of the polluting gases over the specified date range.\n\n### `get_pollution_forecast()`\nFetches air pollution data for the next 5 days for a specific location. The function returns a time series plot of the predicted pollution levels.\n\n## Installation\n\n```bash\n$ pip install airpyllution\n```\n## Usage and Example\n[![readthedocs](https://readthedocs.org/projects/pip/badge/?version=latest)](https://airpyllution.readthedocs.io/en/latest/)\n\n1. Create an [OpenWeather API Key](https://openweathermap.org/appid)\n2. Install airpyllution\n3. Refer to [ReadTheDocs](https://airpyllution.readthedocs.io/en/latest/) for a usage guide and examples.\n\nTo use the package, import the package with the following commands:\n```\nfrom airpyllution.airpyllution import get_air_pollution\nfrom airpyllution.airpyllution import get_pollution_history\nfrom airpyllution.airpyllution import get_pollution_forecast\n```\n\n**Retrieve historic pollution data with specified date range and location:**\n```\nget_pollution_history(1606488670, 1606747870, 49.28, 123.12, api_key)\n```\n\n**Generate an interactive map containing current pollution data by location:**\n\n```\nget_air_pollution(49.28, 123.12, api_key, "Current Air Pollution")\n```\n\n![](docs/air-pollution-map.png)\n\n**Generate a time-series line chart of forecasted air pollution data:**\n```\nimport altair as alt\nalt.renderers.enable("html");\n\nget_pollution_forecast(49.28, 123.12, api_key)\n```\n![](docs/forecast-example.png)\n\n## Contributors \n- Christopher Alexander (@christopheralex)\n- Daniel King (@danfke)\n- Mel Liow (@mel-liow)\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n## License\n\n`airpyllution` was created by Christopher Alexander, Daniel King, Mel Liow. It is licensed under the terms of the [Hippocratic License 3.0](https://github.com/UBC-MDS/airpyllution/blob/main/LICENSE).\n\n## Credits\n\n`airpyllution` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Christopher Alexander, Daniel King, Mel Liow',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

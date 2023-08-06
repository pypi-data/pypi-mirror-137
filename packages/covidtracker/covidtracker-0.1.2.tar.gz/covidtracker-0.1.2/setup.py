# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['covidtracker', 'covidtracker.templates']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.2.0,<5.0.0',
 'geopandas>=0.10.2,<0.11.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'covidtracker',
    'version': '0.1.2',
    'description': 'Provides basic data cleaning, wrangling and plotting of Covid tracking data',
    'long_description': '[![ci-cd](https://github.com/UBC-MDS/Group28-CovidTracker/workflows/ci-cd/badge.svg)](https://github.com/UBC-MDS/Group28-CovidTracker/actions)\n[![codecov](https://codecov.io/gh/UBC-MDS/Group28-CovidTracker/branch/main/graph/badge.svg?token=tKi5DL8bCF)](https://codecov.io/gh/UBC-MDS/Group28-CovidTracker)\n[![Documentation Status](https://readthedocs.org/projects/covidtracker/badge/?version=latest)](https://covidtracker.readthedocs.io/en/latest/?badge=latest)\n\n\n# covidtracker\n\nProvides basic data cleaning, wrangling and plotting of Covid tracking data in Canada.\n\n## Functions\nThe covidtracker package is designed for the easy retrieval and analysis of data pertaining to Covid trends in Canada, including information about cases, vaccinations and testing. The package serves as a wrapper for the opencovid.ca [API](Ihttps://opencovid.ca/api/), and provides additional helper functions for visualising the data, either as a time series or in the form of a map. \n\n* #### `get_covid_data()`\n    Retrieve cleaned and formatted data of specified type and within (optionally) provided time ranges and locations\n\n* #### `plot_time_series()`\n    Function for plotting time series trends in Covid data\n\n* #### `calculate_stat_summary()`\n    Function for returning key statistical information about Covid data, such as long run trends and comparisons between provinces<br>\n\n* #### `plot_geographical()`\n    Function for plotting chloropleth maps with Covid data \n    \n\n## Similar Packages    \nThere are currently no other Python packages available that can perform the same set of data retrieval and analysis functionalities as covidtracker. There are several packages that have similar functionality, but are most are tailored either towards covid data retrieval or data visualization. The packages designed for covid data retrieval also do not use the same data source as covidtracker. Some examples of related Python packages useful for Covid data retrieval and data visualizations include:\n* [covid19dh](https://pypi.org/project/covid19dh/) - For Covid data retrieval\n* [covid](https://pypi.org/project/covid/)- For Covid data retrieval\n* [folium](https://pypi.org/project/folium/) - For data visualizations\n* [plotly](https://pypi.org/project/plotly/) - For data visualizations\n\n\n## Installation\nPlease note that due to GDAL dependencies, the package can only be directly installed on Mac OS and Linux machines. With Windows machine, because `pip install Fiona` does not work, you need to install Fiona package first, and then install our covidtracker package.\n\nMac OS and Linux machine:\n```bash\n$ pip install covidtracker\n```\n\nWindows machine:\n```bash\n$ conda install Fiona\n$ pip install covidtracker\n```\n\n## Usage\n\n```python\nfrom covidtracker.get_covid_data import get_covid_data\nfrom covidtracker.plot_geographical import plot_geographical\nfrom covidtracker.plot_time_series import plot_ts\nfrom covidtracker.calculate_stat_summary import calculate_stat_summary\n\ncovid_df = get_covid_data(\'active\')\nplot_map = plot_geographical(covid_df,\'cumulative_deaths\')\nplot_ts = plot_ts(covid_df, "active_cases")\nsummary = calculate_stat_summary(covid_df, \'active\')\n```\n## Documentation\nDetailed documentation for the package can be found here on Read the Docs : https://covidtracker.readthedocs.io/en/latest/ \n\n## Contributing\n\nWe welcome and recognize all contributions. Please see contributing guidelines in the Contributing document. This repository is currently maintained by\n\n* Cuthbert Chow (@cuthchow)\n* Tianwei Wang (@Davidwang11)\n* Siqi Tao (@SiqiTao)\n* Jessie Wong (@jessie14)\n\n## License\n\n`covidtracker` was created by Group 28. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`covidtracker` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Group 28',
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

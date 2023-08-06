[![codecov](https://codecov.io/gh/UBC-MDS/canadacovidmetrics/branch/main/graph/badge.svg?token=pqqLGsfiXD)](https://codecov.io/gh/UBC-MDS/canadacovidmetrics)
[![ci-cd](https://github.com/UBC-MDS/canadacovidmetrics/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/canadacovidmetrics/actions/workflows/build.yml)
[![Documentation Status](https://readthedocs.org/projects/canada-covid-metrics/badge/?version=latest)](https://canada-covid-metrics.readthedocs.io/en/latest/?badge=latest)

# canadacovidmetrics

This is a Python package that provides key metrics regarding COVID-19 situation in Canada across provinces using the [OpenCovid API](https://opencovid.ca/api/).

## Summary

This package allows users to obtain key metrics on COVID-19 situation in Canada at national or provincial level for a specific time period. The 4 functions will return key metrics, including total cumulative cases, total cumulative deaths, total cumulative recovered cases and total cumulative vaccine completion, using data from [OpenCovid API](https://opencovid.ca/api/). The users may use the key metrics to conduct further analyses on COVID-19 situation in Canada.

## Functions

There are 4 functions in this package:

-   `get_cases` Query total cumulative cases with ability to specify province and date range of returned data.

-   `get_deaths` Query total cumulative deaths with ability to specify province and date range of returned data.

-   `get_recoveries` Query total cumulative recovered cases with ability to specify province and date range of returned data.

-   `get_vaccinations` Query total cumulative vaccine completion with ability to specify province and date range of returned data.

## Installation

```bash
$ pip install canadacovidmetrics
```

## Usage & Examples

### Total number of deaths over past week by province

```python
from canadacovidmetrics import canadacovidmetrics as ccm
import datetime as dt
deaths_last_week = ccm.get_deaths(after=str(dt.date.today() - dt.timedelta(days=7)))
deaths_last_week.groupby('province').sum('deaths').plot.barh(y='deaths', title='Deaths by province in past week');
```

### National vaccination completion in 2021

```python
from canadacovidmetrics import canadacovidmetrics as ccm
vaccines_2021 = ccm.get_vaccinations(loc='canada', after='2021-01-01', before='2021-12-31')
vaccines_2021.plot('date_vaccine_completed', 'cumulative_cvaccine', title='Cumulative national vaccinations');
```

### Daily new case count by province

```python
from canadacovidmetrics import canadacovidmetrics as ccm
cases_data = ccm.get_cases().set_index('date_report')
cases_data.groupby('province')['cases'].plot(legend=True, figsize=(10,6), title='Number of reported cases by day by province');
```

## Python ecosystem

There are several packages for easy access to COVID-19 key metrics or data using different APIs, examples include
- [covid](https://github.com/nf1s/covid) using [John Hopkins University API](https://coronavirus.jhu.edu/about/)
- [COVID19Py](https://github.com/Kamaropoulos/COVID19Py) using [Coronavirus Tracker API](https://github.com/ExpDev07/coronavirus-tracker-api)
- [covid19pyclient](https://github.com/NiklasTiede/covid19pyclient) using [RKI API](https://github.com/marlon360/rki-covid-api)

To our knowledge, there is no similar package using [OpenCovid API](https://opencovid.ca/api/) in the Python ecosystem.

## Documentation

Documentation canadacovidmetrics can be found at [Read the Docs](https://canada-covid-metrics.readthedocs.io/en/latest/)

## Contributors

-   Adam Morphy (@adammorphy)
-   Brandon Lam (@ming0701)
-   Lakshmi Santosha Valli Akella (@valli180)
-   Luke Collins (@LukeAC)

We welcome and recognize all contributions. Please find the guide for contribution in [Contributing Document](https://github.com/UBC-MDS/canadacovidmetrics/blob/main/CONTRIBUTING.md).

## License

`canadacovidmetrics` was created by the Contributors. The dependant API from the COVID-19 Canada Open Data Working Group dataset project has adopted the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) license, which allows freedom of two primary contributions:

**Sharing** — copy and redistribute the material in any medium or format
**Adapting** — remix, transform, and build upon the material
for any purpose, even commercially. 

As contributors to this community, our package has adopted the same creative commons license, in order to enable anyone to share or adapt the Canada Covid Metrics package in R or Python subject to the license.

## Credits

`canadacovidmetrics` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

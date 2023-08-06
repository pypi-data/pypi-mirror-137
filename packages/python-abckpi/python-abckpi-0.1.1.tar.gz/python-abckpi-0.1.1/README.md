# python-abckpi

**Description**: python-abckpi is a library that wraps the ABCKPI REST API to allow a streamlined access to the API main functionalities
such as querying the list of indicators, retrieving data points and setting values of data points

  - **Technology stack**: Python 3, requests, pandas (optional)
  - **Status**:  Beta (0.1.0). The basic functionalities (in particular retrieving and setting data) are available.
  
## Dependencies

python-abckpi depends mainly on Python 3 (currently tested on Python 3.8) and requests. A detailed set of dependencies
is available in [requirements.txt](./ci/requirements.txt)

## Installation

Detailed installation instructions available at [INSTALL](INSTALL.md).

## Usage

To use python-abckpi, you need to the supply the credentials of an ABCKPI account to create an Instance object. The 
functionalities are then available as methods of the Instance object : 

```python
from abckpi.core import Instance
instance = Instance(username=username,
                    password=password)

indicators = instance.get_indicators()
```

The results returned as lists of dictionnaries or as Pandas objects if the pandas dependency is installed.

## Documentation

A complete documentation as well as examples in Jupyter Notebook format are available at 
[Documentation](https://abckpi.gitlab.io/python-abckpi/).


## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Open source licensing info
1. [LICENSE](LICENSE)

----

### Main contributors : 
- Seddik Yassine Abdelouadoud

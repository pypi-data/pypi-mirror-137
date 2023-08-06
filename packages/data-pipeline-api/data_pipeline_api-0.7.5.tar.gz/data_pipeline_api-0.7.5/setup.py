# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_pipeline_api', 'data_pipeline_api.ext']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'h5py>=3.6.0,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'data-pipeline-api',
    'version': '0.7.5',
    'description': 'Python api to interact with the Fair Data Pipeline',
    'long_description': "# pyDataPipeline\n\n[![pyDataPipeline](https://github.com/FAIRDataPipeline/pyDataPipeline/actions/workflows/pyDataPipeline.yaml/badge.svg?branch=dev)](https://github.com/FAIRDataPipeline/pyDataPipeline/actions/workflows/pyDataPipeline.yaml)\n[![codecov](https://codecov.io/gh/FAIRDataPipeline/pyDataPipeline/branch/dev/graph/badge.svg?token=Eax5AmrDxx)](https://codecov.io/gh/FAIRDataPipeline/pyDataPipeline)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5562602.svg)](https://doi.org/10.5281/zenodo.5562602)\n[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/5461/badge)](https://bestpractices.coreinfrastructure.org/projects/5461)\n\nWelcome to pyDataPipeline a Python api to interact with the Fair Data Pipeline.\n\nFull documention of the pyDataPipeline is avaialable at [https://www.fairdatapipeline.org/pyDataPipeline/](https://www.fairdatapipeline.org/pyDataPipeline/)\n\n## Installation\npyDataPipeline can be installed from PyPi:\n```\npip3 install data-pipeline-api\n```\n\nOr from the Repository:\n```\ngit clone https://github.com/FAIRDataPipeline/pythonFDP.git\n\ngit checkout dev\n\npip3 install -e .\n```\n**NB. PyDataPipeline requires Python3.**\n\n## Example submission_script\n\nAssume FDP_CONFIG_DIR, storage_locations and objects have been set by CLI tool\n\n```\nimport os\nimport fairdatapipeline as pipeline\n\ntoken = os.environ.get('FDP_LOCAL_TOKEN')\nconfig_path = os.environ.get('FDP_CONFIG_DIR') + '/config.yaml'\nscript_path = os.environ.get('FDP_CONFIG_DIR') + '/script.sh'\n\nhandle = pipeline.initialise(token, config_path, script_path)\n\npipeline.finalise(token, handle)\n\n```\n\n## SEIRS Model Example\n\nThe SEIRS Model Example is available at: [https://www.fairdatapipeline.org/pyDataPipeline/examples/SEIRS.html](https://www.fairdatapipeline.org/pyDataPipeline/examples/SEIRS.html)\n",
    'author': 'Ryan J Field',
    'author_email': 'ryan.field@glasgow.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.fairdatapipeline.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)

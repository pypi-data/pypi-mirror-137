# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functions',
 'functions.commands',
 'functions.commands.components',
 'functions.components',
 'functions.config',
 'functions.docker',
 'functions.gcp',
 'functions.gcp.cloud_function',
 'functions.gcp.cloud_run']

package_data = \
{'': ['*']}

install_requires = \
['docker>=5.0.2,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.0,<0.5.0']

extras_require = \
{'gcp': ['google-api-python-client>=2.28.0,<3.0.0',
         'google-auth>=2.3.3,<3.0.0',
         'google-cloud-pubsub>=2.8.0,<3.0.0']}

entry_points = \
{'console_scripts': ['functions = functions.main:app']}

setup_kwargs = {
    'name': 'functions-cli',
    'version': '0.1.0a4',
    'description': 'CLI tool for managing your FaaS resources',
    'long_description': "# `functions`\n\n> This package that will get you working with FaaS.\n\n[![DeepSource](https://deepsource.io/gh/Katolus/functions.svg/?label=active+issues&show_trend=true&token=NaMzVnONrQ-lLiofAWpYLilG)](https://deepsource.io/gh/Katolus/functions/?ref=repository-badge)\n\n|   !   | This package is not ready for `production` use. The API is unstabble as it hasn't been released in any major or minor versions of it yet and is constant development. Use it at your own risk and pleasure. <br><br> **Please read the documentation carefully so there are not surprises to state of this project.** |\n| :---: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n\n<!-- ![Logo]() -->\n\n**Outstanding items before the first release can be viewed under [this](https://github.com/users/Katolus/projects/1) project.**\n\n<!-- * Documentation: <https://Katolus.github.io/functions> -->\n* GitHub: <https://github.com/Katolus/functions>\n* PyPI: <https://pypi.org/project/functions-cli/>\n* Free software: MIT\n\n`functions` is a utility package written in Python. It is built to help the developer run, test and deploy FaaS (Function as a Service) resources. Our goal is to combine and simplify efforts required for local and cloud development.\n\nWe are using `docker` as a primary technology to build and orchestrate the functions locally.\n\nTo deploy them to a cloud provider you need to have relevant software pre-installed.\n\n## Features\n\nThe project is still under deep development, and there is still a lot of work to be done even to reach the base quality.\nNonetheless, we believe there is value in using it as it is if it fits your needs and requirements (Python + Linux).\n\nFeedback, issues and request are more than welcome. See how you can [contribute](CONTRIBUTING.md).\n\nSee the road map [document](./docs/roadmap.md) to see how our vision might need your future interest.\n\nHere is a list of functionalities that the package is capable of.\n\n### Locally\n\n* Generate a new template function directories for starting new functions. Two types GCP `http`/`pubsub` - [tutorial](docs/examples/new_gcp_functions.md).\n* Add an existing function to the function registry to be run and deployed as functions native to the package - [tutorial](docs/examples/add_existing_function.md).\n* Build pre-generated, validated and **locally** existing functions using Docker **link to api document**.\n* Operate (`deploy`/`remove`) Google Cloud Platform functions from a local machine - [tutorial](docs/examples/http_function.md).\n* Store information about the built, run and deployed functions locally for reference and configuration - [proposal](docs/proposals/function_registry.md).\n* Print out information about functions and their statuses (Build/Deployed/Running) using the [list](**link to api document**) command.\n* Log function history using a log file stored on your local device - [proposal](docs/proposals/logging.md).\n\n### GCP\n\n* Deploy locally existing function as cloud functions. Limited to two types - `http` and `pubsub`.\n* Delete functions deployed to GCP using this package.\n\n## Compatibility\n\nCurrently the project has been developed and tested only on a Ubuntu OS with **Python 3.9** as the deployment environment. More development is in progress.\n\n## Requirements\n\nThe package is a utility one and it requires underlying software for specific function to be available.\n\nMinimum:\n\n* Python >= `3.8` - for the functioning of the package.\n* `docker` - for running any of the functions locally, you will need to [install docker](https://docs.docker.com/engine/install/).\n\n    ```bash\n    sudo chmod 666 /var/run/docker.sock\n    ```\n\n* [`poetry`](https://python-poetry.org/docs/#installation) - for running the source code locally and code development you need to have this package in the scope.\n\nFor GCP:\n\n* `gcloud` - for deploying to the GCP environment, [install gcloud](https://cloud.google.com/sdk/docs/install).\n\n## Installation\n\nDepending on your use case there are option on how to proceed with installing the package.\nIt is recommended that for regular use, you install the package from `pypi` following the `For use` section.\n\nIf you plan of developing or adjust the code or underlying structures make sure to check out the `For development` section.\n\n### For use\n\nSince it is a regular Python package, available in the main `pypi` repository you can start using it simply by installing the package in your Python environment by running\n\n```bash\npip install functions-cli\n```\n\nin your terminal.\n\n### For development\n\nCheck out the [local development document](docs/local_development.md) for instructions on how get set up.\n\n## Usage\n\nRegardless if you installed the package from the *pypi* repository or from source code, you should be able to invoke the `functions` tool from your command line. The tool has many different commands that should help you building your serverless functions (surprise, otherwise it would be useless...).\n\nHere are a few core ones to get you started. For a full and a comprehensive description of the `CLI` please refer to the [cli document](docs/cli.md).\n\nKeep in mind that the package is in development and all of its structure is a subject to change.\n\n## Creating a new FaaS\n\nThe tool allows you to quickly generate a template of a function that you can the modify to quicken your efforts in producing code.\n\n```bash\nfunctions new http {name_of_the_function}\n```\n\nwill generate you a new `http` like template for your FaaS function in your current directory.\n\n## Building a function\n\nBefore you start working with a function you need make sure it is built and available as a docker image. To do so, run\n\n```bash\nfunctions build {name_of_the_function}\n```\n\n## Running a function locally\n\nIt is great to see what we have created before deploying it to the world. Running...\n\n```bash\nfunctions run {name_of_the_function}\n```\n\nwill start a docker container and expose the function to your locally network on a available port.\n\n**Note**: If you haven't run this function before, you will need to make sure you built (the `build` command) the function first before running.\n\nPlease remember that the container will run as long as you leave it for, so make sure to take it down once you have done all your testing. Running...\n\n```bash\nfunctions stop {name_of_the_function}\n```\n\nshould do the job.\n\n## Deployment it to the cloud\n\nSince we build software to serve us something, we most likely want to deploy it to see it all working and get that full developer satisfaction and availability.\n\nDepending what configuration you had set up, you will be able to deploy your projects to various platforms (extended support pending).\n\nFor example to deploy a function quickly to GCP as a cloud function you want to run...\n\n```bash\nfunctions gcp deploy {path_to_the_function}\n```\n\nWith the correct setup and permissions this should allow you to the deploy a function to the GCP directly from the `functions` cli.\n\n## Remove a function\n\nThis command will remove a function from the local storage, but will not remove the code from the disk.\n\n```bash\nfunctions remove {name_of_the_function}\n```\n\n## Installing autocompletion\n\nCore CLI functionality is built on top of [`Typer`](https://github.com/tiangolo/typer) which means that if you want autocompletion in your scripts follow the instructions derived from there.\n\n```bash\nfunctions --install-completion bash\n```\n\nWith respect to the version of shell you are using.\n\n## Getting help\n\nThe tool is built on brilliant software of others. One of them being `typer`. Thanks to the work of others, you can query the CLI for any useful information by adding `--help` to any of your commands.\n\n```bash\nfunctions run --help\n```\n\nIf you stumble in to any major issue that is not described in the documentation, send a message or create an issue. We will try to help you as soon as it is possible.\n\n## Contributing\n\nIf you are interested in helping out check out the [contributing](./CONTRIBUTING.md) document.\n",
    'author': 'Piotr Katolik',
    'author_email': 'katolus@ventress.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

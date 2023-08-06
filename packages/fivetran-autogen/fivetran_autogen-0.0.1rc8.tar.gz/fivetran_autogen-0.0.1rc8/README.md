# Fivetran Package Config Auto-Generator

[![CircleCI](https://circleci.com/gh/fivetran/dbt_autogen/tree/main.svg?style=svg&circle-token=53f989254370700f10cc8f02e2114cd3fd6e1a5e)](https://circleci.com/gh/fivetran/dbt_autogen/tree/main) [![PyPI version fury.io](https://badge.fury.io/py/fivetran-autogen.svg)](https://pypi.org/project/fivetran-autogen/)

```python
# TODO: Find snappier name
```

The Fivetran Packge Auto-Generator can be used to update your dbt project with the required configuration for Fivetran-created dbt packages.

It will:
* Update your `packages.yml` file
* Update variable configurations in your `dbt_project.yml` file
* Update model/test configurations in your `dbt_project.yml` file (if necessary)

## Installation

Install the auto-generator using pip:

```bash
pip3 install fivetran-autogen==0.0.1rc6      
```

## Usage

### Generating API credentials

The auto-generator uses the Fivetran API to fetch which packages you can install. Follow [these instructions](https://fivetran.com/docs/rest-api/getting-started) to generate your API credentials. These will be required for the next step.

### Running the auto-generator

To user the auto-generator, run the following command **from the root of your dbt project**, i.e. the folder that has your `dbt_project.yml` file:

```bash
fivetran_autogen
```

You will then get prompted to:
* Input your API credentials
* Select which package you want to install
* Answer any package specific questions, i.e. what project/dataset the source data is located in

The auto-generator will query your database to collect information as well, using the profile associated with the dbt project.

### Test the configuration

Once complete, you should see updated changes to your `packages.yml` and `dbt_project.yml` files.

To test out the configuration, run the following commands:

```bash
dbt deps
dbt run
```


from pathlib import Path
from setuptools import setup
from autogen import __version__

here = Path(__file__).parent.resolve()

with (here / "README.md").open(encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="fivetran_autogen",
    version=__version__,
    py_modules=["fivetran_autogen"],
    packages=["autogen", "autogen.packages"],
    include_package_data=True,
    entry_points={"console_scripts": ["fivetran_autogen = autogen.cli:main"]},
    author="Fivetran",
    author_email="hello@fivetran.com",
    url="https://github.com/fivetran/dbt_autogen",
    install_requires=[
        "click==8.0.3",
        "google-cloud-bigquery==2.32.0",
        "google-cloud-bigquery-storage==2.11.0",
        "jsonschema==4.4.0",
        "psycopg2==2.9.3",
        "pyarrow==6.0.1",
        "PyYAML==6.0",
        "requests==2.27.1",
        "ruamel.yaml==0.17.20",
        "snowflake-sqlalchemy==1.3.3",
        "SQLAlchemy==1.4.25",
        "sqlalchemy-bigquery==1.3.0",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)

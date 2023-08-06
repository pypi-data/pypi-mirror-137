==========
SnowFinch
==========
Snowfinch is general purpose python library which allows developers
to quickly convert on prem databases SQL to SnowFlake, perform lightweight ETL,
assist in managing CICD pipelines and  data tokenization.

Why SnowFinch
=============
* Unavailability of any tool for migrating Teradata/MS SQL Server DDLs to Snowflake DDL with constraints
* Time consuming manual process for migrating large number of tables and high volume of data
* Manual validation of migrated data resulting in inaccuracy and inefficiency of the process

Introduction
============
SnowFinch is the tool of choice for
* Schema Mapping and Auto conversion of DDL, Stored procedures, BTEQ scripts
* Dynamic creation of the converted objects on SnowFlake using python connectors DB API
* deploying your artifacts s3 and bitbucket in an automated fashion

Features
########

- `Command-line tool`
- `Python API` - expressive, powerful, and great for working with other packages _ (e.g. `pandas <http://pandas.pydata.org>`_)
- `Config Driven` - manage connection information and credentials securely using the ``snowfinch yaml config`` and ``snowfinch secret`` commands
- `Fully Automated` - Up to 80% automated code conversion to SnowSQL
- `Dynamic Snowflake object creation` - directly performs the DML operation on snowflake
- `CICD` - Uploads the source code to S3  bucket or Bitbucket
- `Tokenization` - Handles tokenization and de-tokenization
- `DBAPI2 Compliant` - DB Driver (Adapter) agnostic. Use your favourite driver that complies with DB-API 2.0
- `S3 Integration` - provides functionality to download and upload data to S3 buckets, and internal stages (Snowflake)

Getting Started
---------------
Assuming that you have Python and ``virtualenv`` installed,
set up your environment and install the required dependencies
like this or you can install the library using ``pip``::

    $ virtualenv snowfinch
    $ source snowfinch/bin/activate
    $ pip install --upgrade setuptools pip
    $ pip install --index-url https://test.pypi.org/simple/ --no-deps snowfinch==0.1.dev3

Install the latest SnowFinch release via pip: ::

    python -m pip install --index-url https://test.pypi.org/simple/ --no-deps snowfinch==0.1.dev3

Using SnowFinch
---------------
After installing SnowFinch

for MS SQL Server: ::

    python  snowfinch.py -c /path/to/snowfinch-app-dev.yaml -p=dev -m=ddl -d=mssql -dt=True
    python  snowfinch.py -c /path/to/snowfinch-app-dev.yaml -p=dev -m=sproc -d=mssql -dt=True
    python  snowfinch.py -c /path/to/snowfinch-app-dev.yaml -p=dev -m=full -d=mssql -dt=True
    python  snowfinch.py -c /path/to/snowfinch-app-dev.yaml -p=dev -m=s3 -d=mssql

for Teradata: ::

    python  snowfinch.py --config /path/to/snowfinch-app-dev.yaml --profile=dev --mode=ddl --dialect=teradata -dt=False
    python  snowfinch.py --config /path/to/snowfinch-app-dev.yaml --profile=dev --mode=sproc --dialect=teradata -dt=True
    python  snowfinch.py --config /path/to/snowfinch-app-dev.yaml --profile=dev --mode=full --dialect=teradata -dt=False
    python  snowfinch.py --config /path/to/snowfinch-app-dev.yaml --profile=dev --mode=s3 --dialect=teradata

Getting Help
------------

Please use the below resources for getting help
* Please email us on the `snowfinch-support@anthem.com`
* Open a SNOW ticket using `snowfinch support`
* If it turns out that you may have found a bug, please `snowfinch issues`
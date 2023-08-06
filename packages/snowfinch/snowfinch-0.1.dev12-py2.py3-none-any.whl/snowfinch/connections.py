import sys

import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from snowfinch.logger import log

logger = log.get_logger()


def snowfinch_connections(dialect, conf):
    conn = None
    if conn is None:
        conn = ''
    if dialect == 'teradata':
        usr = conf['teradata']['user'].get()
        passwd = conf['teradata']['password'].get()
        host = conf['teradata']['host'].get()
        url: str = f'teradatasql://{host}/?user={usr}&password={passwd}&logmech' \
                   f'=LDAP&tmode=TERA&encryptdata=true'

        logger.info(url)

        try:
            logger.info("Connecting to Teradata database...")
            conn = create_engine(url.strip()).connect()
            logger.info("Successfully connected to Teradata.")
        except Exception as err:
            print("Failed to connect to Teradata DB: {}.".format(err))
            raise

    elif dialect == 'snowflake':
        usr = conf['snowflake']['user'].get()
        auth = conf['snowflake']['authenticator'].get()
        try:
            print("Connecting to SnowFlake database...")
            if usr.upper().startswith('SRC') or auth.upper() == 'LOCAL':
                logger.info("Running using Service Account")
                conn = create_engine(URL(
                    account=conf['snowflake']['account'].get(),
                    user=conf['snowflake']['user'].get(),
                    password=conf['snowflake']['password'].get(),
                    database=conf['snowflake']['database'].get(),
                    schema=conf['snowflake']['schema'].get(),
                    warehouse=conf['snowflake']['warehouse'].get(),
                    validate_default_parameters=True
                ))
            else:
                logger.info("Running using HA with external authenticator")
                conn = create_engine(URL(
                    account=conf['snowflake']['account'].get(),
                    user=conf['snowflake']['user'].get(),
                    password=conf['snowflake']['password'].get(),
                    database=conf['snowflake']['database'].get(),
                    schema=conf['snowflake']['schema'].get(),
                    warehouse=conf['snowflake']['warehouse'].get(),
                    authenticator="externalbrowser",
                    validate_default_parameters=True
                ))
                logger.info("Successfully connected to snowflake.")
        except snowflake.connector.errors.DatabaseError as err:
            logger.error("Failed to connect to Snowflake DB: {}.".format(err))
            raise

    elif dialect == 'mssql':
        import pyodbc
        # driver = 'ODBC+Driver+17+for+SQL+Server'
        host = conf['mssql']['host'].get()
        database = conf['mssql']['database'].get()
        usr = conf['mssql']['user'].get()
        passwd = conf['mssql']['password'].get()
        try:
            logger.info("Connecting to MSSQL Server database...")
            # conn = create_engine(conn_url)
            # conn = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
            # conn = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
            # conn = create_engine(conn_str)

            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                  f'SERVER={host};'
                                  f'DATABASE={database};UID={usr};PWD={passwd}')
            logger.info("Successfully connected to MSSQL Server.")
        except Exception as err:
            logger.info("Failed to connect to MSSQL Server DB: {}.".format(err))
            sys.exit(1)
    return conn


def get_source_db_connections(dialect, config):
    # get the source  connection objects
    conn = None

    if conn is None:
        conn = ''

    if dialect == 'mssql':
        conn = snowfinch_connections(dialect, config)

    elif dialect == 'teradata':
        conn = snowfinch_connections(dialect, config)

    elif dialect == 'netezza':
        conn = snowfinch_connections(dialect, config)

    return conn

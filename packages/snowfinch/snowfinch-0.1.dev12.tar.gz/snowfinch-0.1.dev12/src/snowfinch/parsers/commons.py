import re
import ntpath
import os.path
import errno
import pandas as pd
from snowfinch.logger import log
from snowfinch.exceptions import *


logger = log.get_logger()


def get_object_metadata(conn, object_name: str, object_type: str, object_schema: str):
    if object_type == 'table':
        metadata_sql = f"""
        SELECT table_catalog, table_schema, table_owner, table_type, row_count,last_altered
        FROM information_schema.tables 
        WHERE  
            upper(table_schema) = '{object_schema}'
            AND upper(table_name) = '{object_name}';
        """
    elif object_type == 'procedure':
        metadata_sql = f"""
        SELECT procedure_catalog, procedure_schema, procedure_owner, last_altered
        FROM information_schema.procedures 
        WHERE  
            upper(procedure_schema) = '{object_schema}'
            AND upper(procedure_name) = '{object_name}';
        """
    else:
        metadata_sql = ""
        print("Object type currently not part of this method.")

    print(f"\nsql query for {object_schema}.{object_name}")
    print(metadata_sql)
    try:
        print("\nFetching Metadata  from SnowFlake...")
        # object_metadata = conn.execute(metadata_sql).fetchall()
        object_metadata = pd.read_sql(metadata_sql, conn)
        print(object_metadata.transpose())

    except ProgrammingError as err:
        print("ProgrammingError", err)
        raise

    return object_metadata


def get_object_owner(conn, object_name, object_type, object_schema):
    if object_type == 'table':
        owner_query = f"""
        SELECT table_owner as owner
        FROM information_schema.tables
        WHERE
        upper(table_schema) = '{object_schema}'
        AND upper(table_name) = '{object_name}'
        """
    elif object_type == 'procedure':
        owner_query = f"""
        SELECT procedure_owner as owner
        FROM information_schema.procedure
        WHERE
        upper(table_schema) = '{object_schema}'
        AND upper(procedure_name) = '{object_name}'
        """
    else:
        owner_query = ""
        logger.info("Object type currently not part of this method.")

    print(f"\nsql query for {object_schema}.{object_name}")
    print(owner_query)

    try:
        logger.info("\nFetching table owner Metadata from SnowFlake...")
        df = pd.read_sql(owner_query, conn)
        object_owner = ''.join(df['owner'])
        print(f"object_owner: {object_owner}")
    except ProgrammingError as err:
        logger.info("ProgrammingError", err)
        raise
    return object_owner


def grant_ownership(conn, object_name, object_type, object_schema, object_owner):
    if object_type == 'table':
        grant_cmd = f"""
        grant ownership on table {object_schema}.{object_name} to
               role {object_owner} copy current grants;
        """
    elif object_type == 'procedure':
        grant_cmd = f"""
        grant ownership on procedure {object_schema}.{object_name} to
               role {object_owner} copy current grants;
        """
    else:
        grant_cmd = ""
        logger.info("Object type currently not part of this method.")

    logger.info(grant_cmd)
    try:
        print(f"\nChanging the ownership to {object_owner}...")
        conn.execute(grant_cmd)

    except ProgrammingError as err:
        logger.info("ProgrammingError", err)
        raise


def is_word_in_string(word, text):
    pattern = r'(^|[^\w]){}([^\w]|$)'.format(word)
    pattern = re.compile(pattern, re.IGNORECASE)
    matches = re.search(pattern, text)
    return bool(matches)


def read_sql(sql, conn):
    try:
        # read data using a sql query
        _df = pd.read_sql_query(sql, conn)

        # trim columns
        _df = _df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # upper case columns
        _df.columns = [x.upper() for x in _df.columns]
        return _df

    except OperationalError as err:
        logger.Info('Error occurred while executing a query {}'.format(err.args))


# from each line, remove all text which is behind a '--'
def cut_comment(query: str) -> str:
    idx = query.find('--')
    if idx >= 0:
        query = query[:idx]
    return query


def get_sql_stmt_list(file_path, delimiter=';'):
    print(delimiter)
    """
    this function reads one or more SQL statements from a script and returns
    them in a list.

    :param file_path: path to file that contains SQL text to be executed by Snowflake.
    :param delimiter: the delimiter used to separate independent SQL statements.
    :throws: snowflake.connector.errors.ProgrammingError
    :returns: sql statement
    :rtype: str
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        queries = [line.strip() for line in file.readlines()]
        queries = [cut_comment(q) for q in queries]
        sql_command = ' '.join(queries)
        return sql_command


def get_outfile_full_name(_infile, extension):
    filename = ntpath.basename(_infile)
    filepath = ntpath.dirname(_infile)
    out_file_name = filename.split(".")[0]
    out_file = f"{filepath}/{out_file_name}.{extension}"
    return out_file


def silent_remove(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:  # no such file or directory
            raise  # re-raise exception if a different error occurred


def execute_sql_from_file(filename, conn):
    # Execute every command from the input file
    with open(filename, 'r') as fd:
        for command in fd.read().split(';'):
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                conn.execute(command)
            except OperationalError as err:
                logger.error("Command skipped: ", err)

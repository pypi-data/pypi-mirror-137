import sqlalchemy as sa

from snowfinch.constants import *
from snowfinch.connections import *
from snowfinch.parsers.commons import *
from snowfinch.parsers.ddl_generators import *
from snowfinch.exceptions import *

logger = log.get_logger()


def process_snowflake_ddl(df):
    # make column names to uppercase
    df.columns = [x.upper() for x in df.columns]

    df['DDL'] = df['DDL'].str \
        .replace('   ,', ',', regex=True) \
        .replace('   ', ' ', regex=True)
    return df


def drop_table_if_exists(conn, table, schema):
    if check_table_exists(conn, table, schema):
        logger.info("Table exists on snowflake, going ahead with  drop table")

        try:
            conn.execute(f"drop table if exists {schema}.{table}")
            logger.info(f"Successfully dropped the table {table}")
        except ProgrammingError as exc:
            logger.info(f"*"*40)
            logger.warn(exc)
            logger.warn(f"Insufficient privileges to operate on {table}")
            logger.info(f"*"*40)
        except DatabaseError as err:
            logger.error(err)
            logger.info(f"*"*40)
            logger.error(f"Failed dropping the table {table}")
            logger.info(f"*"*40)

    else:
        logger.info("Table does not exists on snowflake, skipping the table drop")


def check_table_exists(conn, table, schema):
    # db = conf['snowflake']['database'].get()
    # schema = conf['snowflake']['schema'].get()
    ins = sa.inspect(conn)
    ret = ins.dialect.has_table(conn.connect(), f"{schema}.{table}")
    print('Table "{}" exists: {}'.format(table, ret))
    return ret


def build_table(dialect, src_conn, tgt_conn, table_list, conf, drop_table=False):
    # get snowflake  parameters
    sf_user = conf['snowflake']['user'].get()
    sf_role = conf['snowflake']['role'].get()
    sf_wh = conf['snowflake']['warehouse'].get()
    sf_db = conf['snowflake']['database'].get()
    sf_table_owner_role = conf['snowflake']['owner_role'].get()
    sf_schema = conf['snowflake']['schema'].get()
    src_db = conf[dialect]['database'].get()
    add_audit_cols = conf['snowflake']['add_audit_cols'].get()
    obj_typ = 'table'

    try:
        with src_conn as s_conn, tgt_conn.connect() as t_conn:
            for table in table_list:
                if "." in table:
                    src_db = table.split('.')[0]
                    src_table = table.split('.')[1]
                else:
                    src_db = src_db
                    src_table = table

                if src_table.startswith(tuple(STG_SCHEMA_PRFX_LIST)):
                    _sf_schema = f"{sf_schema}_STG"
                elif src_table.endswith(tuple(QA_SCHEMA_PRFX_LIST)):
                    _sf_schema = f"{sf_schema}_QADATA"
                else:
                    _sf_schema = sf_schema

                logger.info(f"\nCreating {src_table} on Snowflake @{_sf_schema}...")
                logger.info("snowflake table: " + src_table)
                logger.info("snowflake database: " + sf_db)
                logger.info("snowflake schema: " + _sf_schema)

                # table exist
                table_exists = check_table_exists(t_conn, src_table, _sf_schema)
                logger.info("checking if table exist...")
                logger.info(f"*" * 40)
                if table_exists:
                    logger.warn(f"table {src_table} already exists in snowflake!!")
                    if drop_table:
                        logger.warn(f"table exists but drop_table is true!!")
                        logger.warn(f"dropping the table...")
                        logger.info("")
                        logger.info("checking the table grants...")
                        owner = get_object_owner(t_conn, src_table, obj_typ, _sf_schema)
                        logger.info(f"owner: {owner}")
                        logger.info("")
                        if not (owner == sf_role or owner == sf_table_owner_role):
                            logger.warn(f"user {sf_user} does not have the privileges to drop the table")
                            logger.warn(f"please check with {owner} to drop this table!!")
                        else:
                            logger.info("dropping the table...")
                            drop_table_if_exists(t_conn, src_table, _sf_schema)
                            logger.info("")
                    else:
                        logger.warn(f"table exists but drop_table is false!!")
                        logger.warn(f"drop_table=False, hence skipping the ddl creation!!")
                        logger.info("")
                else:
                    logger.info(f"table {src_table} doesn't exists in snowflake!!")
                    logger.info(f"generating the ddl for  {src_table}...")

                    # Generate DDL
                    logger.info("generating the table ddl...")
                    logger.info(f"*" * 40)
                    ddl_sql = get_ddl(dialect, src_db, _sf_schema, src_table)

                    # get the SnowFlaked DDL
                    raw_df = read_sql(ddl_sql, s_conn)
                    logger.info("ddl row count: ", len(raw_df.index))
                    logger.info("checking is the table exist on source...")
                    logger.info("")
                    if len(raw_df.index) == 0:
                        logger.error(f"{src_table} does not exist on source DB, Please check!!\n")
                        logger.info("")
                    else:
                        # transform the DDL
                        logger.info("transforming the ddl...")
                        final_df = process_snowflake_ddl(raw_df)
                        logger.info(final_df)
                        logger.info("")

                        # convert DDL to a list
                        logger.info("converting the ddl to a list...")
                        lst1 = final_df['DDL'].astype(str).tolist()
                        logger.info(lst1)
                        logger.info("")

                        audit_col_list = [
                            'EDL_RUN_ID VARCHAR(255) NOT NULL COLLATE \'utf8\' DEFAULT \'NA\',',
                            'EDL_SCRTY_LVL_CD VARCHAR(10) NOT NULL COLLATE \'utf8\' DEFAULT \'NA\',',
                            'EDL_LOB_CD VARCHAR(10) NOT NULL COLLATE \'utf8\' DEFAULT \'NA\',',
                            'EDL_EXTRNL_LOAD_CD VARCHAR(10) NOT NULL COLLATE \'utf8\' DEFAULT \'NA\',',
                            'EDL_SOR_CD VARCHAR(10) NOT NULL COLLATE \'utf8\' DEFAULT \'NA\',',
                            'EDL_LOAD_DTM TIMESTAMP_NTZ(9) NOT NULL DEFAULT CAST(\'8888-12-31 00:00:00\' AS '
                            'TIMESTAMP_NTZ(9)) ,'
                        ]
                        if add_audit_cols == "Y":
                            logger.info("add_audit_cols=Y, Adding EDL audit columns...")
                            _index = lst1[0].index('(') + 1
                            l1 = [f'CREATE TABLE IF NOT EXISTS {_sf_schema}.{src_table} (']
                            logger.info(l1)
                            # remove the l1 from first element
                            lst1[0] = lst1[0][_index:]
                            # copy the list
                            lst2 = lst1[:]
                            logger.info(lst2)
                            # add the audit columns to the list2
                            lst2[0:0] = audit_col_list[:]
                            logger.info(lst2)
                            # lst3 = lst2[:]
                            # lst3[0] = l1 + lst
                            lst = l1 + lst2
                        else:
                            logger.info("Audit Columns Flag is N, Skipping the audit column additions")
                            lst = lst1

                        # clean the create table statement
                        create_table_stmt = '\n'.join(map(str, lst))
                        logger.info("create_table_stmt....")
                        logger.info(create_table_stmt)

                        # drop table - optional
                        # if drop_table:
                        #     logger.info("check the table grants")
                        #     # grant_ownership(src_table, _sf_schema, sf_table_owner_role, t_conn)
                        #     owner = get_object_owner(t_conn, src_table, obj_typ, _sf_schema)
                        #     logger.info(owner)
                        #     if not (owner == sf_role or owner == sf_table_owner_role):
                        #         logger.info(f"user {sf_user} does not have the privileges to drop the table")
                        #     else:
                        #         drop_table_if_exists(t_conn, src_table, _sf_schema)

                        # Execute the create table statement
                        logger.info("executing the ddl on snowflake...")
                        logger.info(f"*" * 40)
                        t_conn.execute(f'use warehouse {sf_wh}')
                        t_conn.execute(f'use database {sf_db}')
                        t_conn.execute(f'use schema {_sf_schema}')
                        logger.info(f"Creating {src_table}")
                        t_conn.execute(f"""
                              {create_table_stmt}
                          """)
                        # Change the ownership of the table
                        grant_ownership(t_conn, src_table, obj_typ, _sf_schema, sf_table_owner_role)
                        # Check the table metadata to confirm  table creation and ownership
                        om = get_object_metadata(t_conn, src_table, obj_typ, _sf_schema)
                        logger.info(om)
                        logger.info(f"Successfully created {src_table} on SnowFlake\n")
    except Exception as exc:
        logger.exception(exc)

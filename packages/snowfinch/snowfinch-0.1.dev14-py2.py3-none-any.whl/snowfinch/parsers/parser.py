from __future__ import print_function

from snowfinch.sshclient import RemoteClient
from snowfinch.parsers.bteqparser import *
from snowfinch.parsers.ddlparser import *
from snowfinch.parsers.sproc_parser import *
from snowfinch.connections import snowfinch_connections
from snowfinch.aws.s3upload import s3_uploader
from snowfinch.logger import log

logger = log.get_logger()


def get_s3_upload(_config):
    script_dir = _config['bteq']['script_dir'].get()
    script_name = _config['bteq']['source_files'].get()
    s3_bucket = _config['s3']['s3_bucket'].get()
    s3_key = _config['s3']['s3_key'].get()
    s3_profile = _config['s3']['s3_profile'].get()

    if script_name is None:
        logger.info(f"Uploading all SnowFinch SQL from the input dir")
        local_file = script_dir + "/*.sql"
    else:
        logger.info(f"Uploading a single Snowfinch SQL file")
        infile = script_dir + "/" + script_name

        local_file = get_outfile_full_name(infile, 'sql')

    logger.info(f"input scripts dir: {script_dir}")
    logger.info(f"input scripts name: {script_name}\n")
    logger.info(f"input scripts name and path: {local_file}\n")

    try:
        logger.info(f"Uploading the SnowFinch SQL to S3\n")
        s3_uploader(local_file, s3_key, s3_bucket, s3_profile)
        logger.info(f"Successfully uploaded the SnowFinch SQL files to S3\n")
    except Exception as ex:
        logger.error(ex)


def get_scp_to_local(host, user, passwd, ssh_key, remote_dir, download_dir, remote_files):
    # get ssh client
    client = RemoteClient(host, user, passwd, ssh_key, remote_dir)
    # download the files from remote to local
    with client.scp as scp:
        # Downloading a file from remote machine
        for file in remote_files:
            remote_file = remote_dir + file
            local_file = download_dir + file
            scp.get(remote_file, local_file)


def get_scp_to_remote(host, user, passwd, ssh_key, local_dir, upload_dir, local_files):
    client = RemoteClient(host, user, passwd, ssh_key, upload_dir)
    with client.scp as scp:
        # Downloading a file from remote machine
        # Uploading file from local to remote machine
        for local_file in local_files:
            local_file = local_dir + local_file
            scp.put(local_file, upload_dir)


def get_bteq_build(_config):
    script_dir = _config['bteq']['script_dir'].get()
    script_name = _config['bteq']['source_files'].get()
    logger.info(f"input scripts dir: {script_dir}")
    logger.info(f"input scripts name: {script_name}\n")
    if script_name is None:
        infile = script_dir
    else:
        infile = script_dir + "/" + script_name
    logger.info(f"infile: {infile}")
    build_sql(infile, _config)


def get_ddl_build(dialect, _config, drop_table=False):
    # get the target(snowflake)  connection objects
    tgt_conn = snowfinch_connections("snowflake", _config)

    # get the source(teradata,mssql)  connection objects
    src_conn = get_source_db_connections(dialect, _config)

    src_table_list = _config[dialect]['tablelist'].get()

    # get_ddl_conversion(tgt_conn, src_conn, configs, td_table_list)
    build_table(dialect, src_conn, tgt_conn, src_table_list, _config, drop_table=drop_table)


def get_filenames(directory, exclude=None, include=None, concurrency=1,  split=False):
    """
    Return a list of filenames to upload, filtered by :attr:`include` and
    :attr:`exclude`, if set.

    If `split` is ``True``, then this method returns a list of lists, where
    filenames are evenly divided into :attr:`concurrency` groups.

    After running this method, :attr:`total` will be set to the number of
    filenames found.

    """
    filenames = []
    total = 0
    for path, dirs, files in os.walk(directory):
        for filename in files:
            filename = os.path.join(path, filename)
            # Iterate over all the include regexes, determining if we
            # should include this filename
            if include:
                skip = True
                for reg in include:
                    if reg.search(filename):
                        skip = False
                        break
                if skip:
                    continue
            # Iterate over the exclude regexes, seeing if we should skip
            if exclude:
                skip = False
                for reg in exclude:
                    if reg.search(filename):
                        skip = True
                        break
                if skip:
                    continue
            filenames.append(filename)
            total += 1

    if split:
        groups = [list() for _ in range(concurrency)]
        for i in range(len(filenames)):
            groups[i % concurrency].append(filenames[i])
        filenames = groups

    return filenames


def get_sproc_build(dialect, _config):
    if dialect == 'mssql':
        build_sproc_mssql(_config)
    else:
        logger.info("Stored procedure currently supported for msql only")


def get_full_build(dialect, _config, drop_table=False):
    script_source = _config['bteq']['source'].get()
    script_dir = _config['bteq']['script_dir'].get()
    script_names = _config['bteq']['source_files'].get()
    logger.info(f"input scripts dir: {script_dir}")
    infile_list = None
    if script_names is None:
        logger.info(f"input scripts list is  empty")
        logger.info(f"input scripts source is {script_source}")

        if script_source.lower() == "remote":
            logger.info(f"remote input scripts dir: {script_dir}")

            # get ssh config
            local_dir = _config['bteq']['download_dir'].get()
            host_name = _config['bteq']['remote_host'].get()
            user_name = _config['bteq']['remote_user'].get()
            pass_word = _config['bteq']['remote_password'].get()
            ssh_key = _config['bteq']['ssh_key_path'].get()
            remote_files = "{local_dir}/*"
            # download the remote files to local
            get_scp_to_local(host_name, user_name, pass_word, ssh_key, script_dir, local_dir, remote_files)
            # shutil.rmtree(dirpath)
        else:
            logger.info(f"input scripts source is {script_source}")
            infile_list = get_filenames(script_dir)
    else:
        logger.info(f"input scripts files: {script_names}")
        infile_list = [os.path.join(script_dir, name) for name in script_names]

    logger.info(infile_list)

    logger.info("creating source and target connections ...\n")
    tgt_conn = snowfinch_connections("snowflake", _config)

    # get the source  connection objects
    src_conn = get_source_db_connections(dialect, _config)

    logger.info("\nConverting Teradata BTEQ to SnowSQL...")

    for file in infile_list:
        logger.info(f"\ninput script to be converted: {file}")

        # get the VT list
        volatile_table_list = get_volatile_table_list(file)
        print("\nVolatile Tables List....")
        print(*volatile_table_list, sep='\n')

        # Get the source tables
        source_table_list = get_source_table_list(file)
        print("\nSource Tables List...")
        print(*source_table_list, sep='\n')

        # get only not  vt tables
        if volatile_table_list:
            logger.info("Volatile tables found, removing them from exist check..")
            src_table_list = list(set(source_table_list) - set(volatile_table_list))
        else:
            logger.info("No Volatile tables seen in the input script")
            src_table_list = source_table_list

        print("\nFinal Table List...")
        print(*src_table_list, sep='\n')

        if src_table_list:
            build_table(dialect, src_conn, tgt_conn, src_table_list, _config, drop_table=drop_table)
        else:
            logger.info("All tables are volatile table, Skipping the table exist")

        # build snowflake sql from Teradata
        build_sql(file, _config)

        # finally, upload the sql to s3
        get_s3_upload(_config)

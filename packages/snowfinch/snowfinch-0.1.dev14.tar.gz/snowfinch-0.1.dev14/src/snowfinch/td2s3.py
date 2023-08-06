import pandas as pd
import yaml
import boto3
from io import StringIO
from io import BytesIO
from sqlalchemy import create_engine
import logging

logger = logging.getLogger("tera2s3")
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def td_connect(config):
    usr = config['teradata'].get('user')
    passwd = config['teradata'].get('password')
    host = config['teradata'].get('host')
    url: str = f'teradatasql://{host}/?user={usr}&password={passwd}&logmech' \
               f'=LDAP&tmode=TERA&encryptdata=true'
    print(url)
    try:
        logger.info("Connecting to Teradata database...")
        conn = create_engine(url.strip()).connect()
        logger.info("Successfully connected to Teradata.")
        return conn
    except Exception as err:
        print("Failed to connect to Teradata DB: {}.".format(err))
        raise


def pad_left(n, width, pad="0"):
    return ((pad * width) + str(n))[-width:]


def load_yaml(conf_file):
    with open(conf_file, "r") as cf:
        return yaml.full_load(cf)


def copy_to_s3(df, bucket, filepath, fmt, s3profile):
    boto3.setup_default_session(profile_name=s3profile)
    client = boto3.client('s3')
    if fmt == 'parquet':
        out_buffer = BytesIO()
        df.to_parquet(out_buffer, index=False, compression='snappy', engine='pyarrow')
    elif fmt == 'csv':
        out_buffer = StringIO()
        df.to_csv(out_buffer, header=True, index=False)
    out_buffer.seek(0)
    # csv_buf = StringIO()
    # df.to_csv(csv_buf, header=True, index=False)
    # csv_buf.seek(0)
    client.put_object(Bucket=bucket, Body=out_buffer.getvalue(), Key=filepath)
    print(f'Copy {df.shape[0]} rows to S3 Bucket {bucket} at {filepath}, Done!')


def get_counts(chunk):
    voters_street = chunk[
        "Residential Address Street Name "]
    return voters_street.value_counts()


if __name__ == '__main__':
    app_config_file = '/Users/AG29266/Library/Application Support/JetBrains/PyCharm2021.2/scratches/scratch.yml'
    config = load_yaml(app_config_file)
    tdc = td_connect(config)
    url = "jdbc:teradata://DWPROD2COP1.CORP.ANTHEM.COM/database=etl_views_prov_adl,tmode=TERA,charset=UTF8, logmech=LDAP"
    driver = "com.teradata.jdbc.TeraDriver"

    properties = {
        "user": config['teradata'].get('user'),
        "password": config['teradata'].get('password'),
        "driver": driver
    }

    sql_query = "select * from edw_allphi.sps_cd_val_trnsltn"
    table_name = "sps_cd_val_trnsltn"
    count = 0
    # for chunk in pd.read_sql_query(clm_hist_sql, tdc, chunksize=1000000):
    #     copy_to_s3(chunk,
    #                'antm-sf-sit-dataz-nogbd-phi-useast1',
    #                'cnfz/edlc01/rdm/edw/fncl_prod_cf/snowfinch_part_%s.parquet' % pad_left(count,4),
    #                'parquet',
    #                'aws-dev-pt')
    #     count += 1
    s3_source_bucket_clm = "antm-pt-sit-dataz-nogbd-nophi-useast1"
    s3_source_path_clm = "cnfz/edlc01/prov/edw/"

    for chunk in pd.read_sql_query(sql_query, tdc, chunksize=2000000):
        copy_to_s3(chunk,
                   s3_source_bucket_clm,
                   f'{s3_source_path_clm}/{table_name}/snowfinch_part_%s.snappy.parquet' % pad_left(count, 4),
                   'parquet',
                   'aws-dev-pt')
        count += 1



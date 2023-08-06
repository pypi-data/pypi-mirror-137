import pandas as pd
import yaml
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import boto3
from io import StringIO
from io import BytesIO


def read_sql(sql, conn):
    try:
        # read data using a sql query
        df = pd.read_sql_query(sql, conn)

        # trim columns
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # upper case columns
        df.columns = [x.upper() for x in df.columns]

    except Exception as err:
        print('Error occurred while executing a query {}'.format(err.args))

    return df


def load_yaml(conf_file):
    with open(conf_file, "r") as cf:
        return yaml.full_load(cf)


def pad_left(n, width, pad="0"):
    return ((pad * width) + str(n))[-width:]


def copy_to_s3(df, bucket, filepath, fmt, s3profile):
    boto3.setup_default_session(profile_name=s3profile)
    client = boto3.client('s3')

    if fmt == 'parquet':
        out_buffer = BytesIO()
        df.to_parquet(out_buffer, index=False, compression='snappy')

    elif fmt == 'csv':
        out_buffer = StringIO()
        df.to_csv(out_buffer, header=True, index=False)

    out_buffer.seek(0)

    # csv_buf = StringIO()
    # df.to_csv(csv_buf, header=True, index=False)
    # csv_buf.seek(0)

    client.put_object(Bucket=bucket, Body=out_buffer.getvalue(), Key=filepath)
    print(f'Copy {df.shape[0]} rows to S3 Bucket {bucket} at {filepath}, Done!')


if __name__ == '__main__':
    config = load_yaml('/Users/ag29266/PycharmProjects/cloudflow/config/pt-inntwk-wgs.yaml')
    # Set options below

    conn = create_engine(URL(
        account='eda_prod.anthemdatalake.us-east-1.privatelink',
        user='AN118647AD',
        database='P01_EDL',
        schema="EDL_ALLPHI",
        warehouse="P01_EDL_USER_WH_M",
        authenticator="externalbrowser",
        validate_default_parameters=True
    ))
    # ein = read_sql(q, conn)
    # ein.to_csv(r'/Users/ag29266/Downloads/MBRSHP_WGS_WGMGRPR.csv', index=False, header=True)
    # ep_rltnshp = read_sql("select * from ep_rltnshp", conn)
    # print(ep_rltnshp.head())

    # copy_to_s3(ep_rltnshp,
    #            'antm-sf-sit-dataz-nogbd-phi-useast1',
    #            'cnfz/edlc01/prov/edw/ep_rltnshp/mbrshp_wgs_wgmgrpr.parquet',
    #            'parquet',
    #            'aws-dev-pt')

    count = 0
    table_name = "sps_cd_val_trnsltn"
    query = "select * from sps_cd_val_trnsltn"

    s3_source_bucket = "antm-sf-sit-dataz-nogbd-phi-useast1"
    s3_source_path = "cnfz/edlc01/clm/edw"

    for chunk in pd.read_sql_query(query, conn, chunksize=1500000):
        copy_to_s3(chunk,
                   s3_source_bucket,
                   f's3_source_path/{table_name}/snowfinch_part_%s.snappy.parquet' % pad_left(count, 4),
                   'parquet',
                   'aws-prod-exec')
        count += 1










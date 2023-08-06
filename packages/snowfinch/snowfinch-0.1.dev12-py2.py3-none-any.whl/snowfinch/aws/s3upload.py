import os
import boto3


def s3_uploader(localdir, s3dir, s3bucket, s3profile):
    boto3.setup_default_session(profile_name=s3profile)
    client = boto3.client('s3')

    # enumerate local files recursively
    for root, dirs, files in os.walk(localdir):
        for filename in files:
            # construct the full local path
            local_path = os.path.join(root, filename)
            print("local path", local_path)

            # construct the full  path
            relative_path = os.path.relpath(local_path, localdir)
            print("relative path", relative_path)
            s3_path = os.path.join(s3dir, relative_path)

            # relative_path = os.path.relpath(os.path.join(root, filename))

            print('Searching "%s" in "%s"' % (s3_path, s3bucket))
            try:
                client.head_object(Bucket=s3bucket, Key=s3_path)
                print("Path found on S3! Skipping %s..." % s3_path)

                # try:
                # client.delete_object(Bucket=bucket, Key=s3_path)
                # except:
                # print "Unable to delete %s..." % s3_path
            except Exception as ex:
                print("Uploading %s...", s3_path, ex)
                client.upload_file(local_path, s3bucket, s3_path)


# if __name__ == '__main__':
# # initiate the configuration
# configs = confuse.Configuration('SnowFinch', __name__)
#
# # Add conf items from specified file
# configs.set_file('/Users/ag29266/Downloads/pims/snowfinch-vbc-dev.yaml')
# profile = f"{configs['profile']}"
#
# s3_bucket = configs[profile]['s3']['s3_bucket'].get()
# s3_key = configs[profile]['s3']['s3_key'].get()
# s3_profile = configs[profile]['s3']['s3_profile'].get()
# local_dir = configs[profile]['s3']['localdir'].get()
#
# # s3_bucket_name = 'antm-481935479534-ssm-dev-filetransfer'
# # s3_key = 'SnowFinch/'
# # local_directory = '/Users/ag29266/Downloads/pims'
#
# # configs = configparser.RawConfigParser()
# # path = pathlib.PosixPath('~/.aws/credentials')
# # configs.read(path.expanduser())
# # profile = 'aws-dev-vbc'
# # upload_to_aws(outfile, s3_bucket_name, s3_key, configs, profile)
#
# # get an access token, local (from) directory, and S3 (to) directory
# # from the command-line
# upload_dir_to_s3(local_dir, s3_key, s3_bucket, s3_profile)

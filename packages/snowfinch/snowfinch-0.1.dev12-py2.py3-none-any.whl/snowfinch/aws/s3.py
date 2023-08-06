from boto3 import Session
from boto3.s3.transfer import TransferConfig
from botocore.client import Config
from snowfinch.exceptions import *
from snowfinch.aws.s3utils import ProgressPercentage
from snowfinch.constants import *
from snowfinch.logger import log

logger = log.get_logger()


class S3(object):

    def __init__(self, profile=None, kms_key=None, **kwargs):

        self.profile = profile
        self.kms_key = kms_key
        self.session = None
        self.s3 = None

        self._set_session()
        self._set_client()

    def _set_session(self):
        try:
            self.session = Session(profile_name=self.profile)
            logger.info("Initialized AWS session.")
        except Exception as e:
            logger.error("Error initializing AWS Session, err: %s", e)
            raise S3Error("Error initializing AWS Session.")
        credentials = self.session.get_credentials()
        if credentials is None:
            raise S3CredentialsError("Credentials could not be set.")

    def _set_client(self):
        try:
            self.s3 = self.session.client("s3", config=Config(signature_version="s3v4"))
            logger.info("Successfully initialized S3 client.")
        except Exception as e:
            logger.error("Error initializing S3 Client, err: %s", e)
            raise S3InitializationError("Error initializing S3 Client.")

    def _credentials_string(self):
        creds = self.session.get_credentials()
        if creds.token is not None:
            temp = "aws_access_key_id={};aws_secret_access_key={};token={}"
            return temp.format(creds.access_key, creds.secret_key, creds.token)
        else:
            temp = "aws_access_key_id={};aws_secret_access_key={}"
            return temp.format(creds.access_key, creds.secret_key)

    @staticmethod
    def _generate_s3_path(bucket, key):
        return "s3://{0}/{1}".format(bucket, key)

    @staticmethod
    def _generate_unload_path(bucket, folder):
        if folder:
            s3_path = "s3://{0}/{1}".format(bucket, folder)
        else:
            s3_path = "s3://{0}".format(bucket)
        return s3_path

    def upload_to_s3(self, local, bucket, key):
        extra_args = {}
        try:
            # force ServerSideEncryption
            if self.kms_key is None:
                extra_args["ServerSideEncryption"] = "AES256"
                logger.info("Using AES256 for encryption")
            else:
                extra_args["ServerSideEncryption"] = "aws:kms"
                extra_args["SSEKMSKeyId"] = self.kms_key
                logger.info("Using KMS Keys for encryption")

            logger.info("Uploading file to S3 bucket: %s", self._generate_s3_path(bucket, key))
            self.s3.upload_file(
                local, bucket, key, ExtraArgs=extra_args, Callback=ProgressPercentage(local)
            )
        except Exception as e:
            logger.error("Error uploading to S3. err: %s", e)
            raise S3UploadError("Error uploading to S3.")

    def upload_list_to_s3(self, local_list, bucket, folder=None):
        output = []
        for file in local_list:
            if folder is None:
                s3_key = os.path.basename(file)
            else:
                s3_key = "/".join([folder, os.path.basename(file)])
            self.upload_to_s3(file, bucket, s3_key)
            output.append("/".join([bucket, s3_key]))
        return output

    def download_from_s3(self, bucket, key, local):
        try:
            logger.info(
                "Downloading file from S3 bucket: %s", self._generate_s3_path(bucket, key),
            )
            config = TransferConfig(max_concurrency=5)
            self.s3.download_file(bucket, key, local, Config=config)
        except Exception as e:
            logger.error("Error downloading from S3. err: %s", e)
            raise S3DownloadError("Error downloading from S3.")

    def download_list_from_s3(self, s3_list, local_path=None):
        if local_path is None:
            local_path = os.getcwd()

        output = []
        for f in s3_list:
            s3_bucket, key = self.parse_s3_url(f)
            local = os.path.join(local_path, os.path.basename(key))
            self.download_from_s3(s3_bucket, key, local)
            output.append(local)
        return output

    def delete_from_s3(self, bucket, key):
        try:
            logger.info("Deleting file from S3 bucket: %s", self._generate_s3_path(bucket, key))
            self.s3.delete_object(Bucket=bucket, Key=key)
        except Exception as e:
            logger.error("Error deleting from S3. err: %s", e)
            raise S3DeletionError("Error deleting from S3.")

    def delete_list_from_s3(self, s3_list):

        for file in s3_list:
            s3_bucket, s3_key = self.parse_s3_url(file)
            self.delete_from_s3(s3_bucket, s3_key)

    @staticmethod
    def parse_s3_url(s3_url):
        temp_s3 = s3_url.replace("s3://", "")
        s3_bucket = temp_s3.split("/")[0]
        s3_key = "/".join(temp_s3.split("/")[1:])
        return s3_bucket, s3_key

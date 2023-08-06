import os
from pathlib import PurePath
from .exceptions import DBError, S3CredentialsError
from .aws.s3 import S3
from .logger import log

logger = log.get_logger()

COPY_FORMAT_OPTIONS = {
    "csv": {
        "compression",
        "record_delimiter",
        "field_delimiter",
        "skip_header",
        "date_format",
        "time_format",
        "timestamp_format",
        "binary_format",
        "escape",
        "escape_unenclosed_field",
        "trim_space",
        "field_optionally_enclosed_by",
        "null_if",
        "error_on_column_count_mismatch",
        "validate_utf8",
        "empty_field_as_null",
        "skip_byte_order_mark",
        "encoding",
    },
    "json": {
        "compression",
        "file_extension",
        "enable_octal",
        "allow_duplicate",
        "strip_outer_array",
        "strip_null_values",
        "ignore_utf8_errors",
        "skip_byte_order_mark",
    },
    "parquet": {"binary_as_text"},
}


UNLOAD_FORMAT_OPTIONS = {
    "csv": {
        "compression",
        "record_delimiter",
        "field_delimiter",
        "file_extension",
        "date_format",
        "time_format",
        "timestamp_format",
        "binary_format",
        "escape",
        "escape_unenclosed_field",
        "field_optionally_enclosed_by",
        "null_if",
    },
    "json": {"compression", "file_extension"},
    "parquet": {"snappy_compression"},
}


def combine_options(options=None):
    """ Returns the ``copy_options`` or ``format_options`` attribute with spaces in between and as
    a string. If options is ``None`` then return an empty string.
    """
    return " ".join(options) if options is not None else ""


class Fincher(S3):
    def __init__(self, profile=None, conn=None):
        self.conn = conn
        try:
            S3.__init__(self, profile)
        except S3CredentialsError:
            logger.warning("S3 credentials were not found. S3 functionality is disabled")
            logger.warning("Only internal stages are available")

    def upload_to_stage(self, local, stage, parallel=4, auto_compress=True, overwrite=True):
        local_uri = PurePath(local).as_posix()
        self.conn.execute(
            "PUT 'file://{0}' {1} PARALLEL={2} AUTO_COMPRESS={3} OVERWRITE={4}".format(
                local_uri, stage, parallel, auto_compress, overwrite
            )
        )

    def download_from_stage(self, stage, local=None, parallel=10):
        if local is None:
            local = os.getcwd()
        local_uri = PurePath(local).as_posix()
        self.conn.execute("GET {0} 'file://{1}' PARALLEL={2}".format(stage, local_uri, parallel))

    def load(self, table_name, stage, file_type="csv", format_options=None, copy_options=None):
        if not self.conn:
            raise DBError("No Snowflake connection object is present.")

        if file_type not in COPY_FORMAT_OPTIONS:
            raise ValueError(
                "Invalid file_type. Must be one of {0}".format(list(COPY_FORMAT_OPTIONS.keys()))
            )

        if format_options is None and file_type == "csv":
            format_options = ["FIELD_DELIMITER='|'", "SKIP_HEADER=0"]

        format_options_text = combine_options(format_options)
        copy_options_text = combine_options(copy_options)
        base_copy_string = "COPY INTO {0} FROM '{1}' " "FILE_FORMAT = (TYPE='{2}' {3}) {4}"
        try:
            sql = base_copy_string.format(
                table_name, stage, file_type, format_options_text, copy_options_text
            )
            self.conn.execute(sql, commit=True)

        except Exception as e:
            logger.error("Error running COPY on Snowflake. err: %s", e)
            raise DBError("Error running COPY on Snowflake.")

    def unload(
        self,
        stage,
        table_name,
        file_type="csv",
        format_options=None,
        header=False,
        copy_options=None,
    ):

        if not self.conn:
            raise DBError("No Snowflake connection object is present")

        if file_type not in COPY_FORMAT_OPTIONS:
            raise ValueError(
                "Invalid file_type. Must be one of {0}".format(list(UNLOAD_FORMAT_OPTIONS.keys()))
            )

        if format_options is None and file_type == "csv":
            format_options = ["FIELD_DELIMITER='|'"]

        format_options_text = combine_options(format_options)
        copy_options_text = combine_options(copy_options)
        base_unload_string = (
            "COPY INTO {0} FROM {1} " "FILE_FORMAT = (TYPE='{2}' {3}) HEADER={4} {5}"
        )

        try:
            sql = base_unload_string.format(
                stage, table_name, file_type, format_options_text, header, copy_options_text
            )
            self.conn.execute(sql, commit=True)
        except Exception as e:
            logger.error("Error running UNLOAD on Snowflake. err: %s", e)
            raise DBError("Error running UNLOAD on Snowflake.")

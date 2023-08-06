"""
Functions for exception manipulation + custom exceptions used by SnowFinch
to identify common deviations from the expected behavior.
"""
import functools
import logging
import sys
import traceback


class SnowFinchBaseError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class ConfigurationError(SnowFinchBaseError):
    """
    For use with configuration file handling.
    """
    pass


class FileNotFound(SnowFinchBaseError):
    """
    Raised when file does not exist.
    """
    pass


class ConfigNotFound(ConfigurationError, FileNotFound):
    """
    Raised when the specified configuration file does not exist.
    """
    pass


class ConnectionLock(ConfigurationError):
    """
    Raised when connection is locked by invalid attempts and the
    'protect' feature is being used.
    """

    def __init__(self, dsn):
        super(ConnectionLock, self).__init__(("Connection {0} is currently locked. please update "
                                              "credentials and run:\n\tsnowfinch config --unlock {0}").format(dsn))


class ConfigReadOnly(ConfigurationError):
    """
    Raised when a write is attempted on a configuration file was opened
    in read mode.
    """
    pass


class MissingPackage(SnowFinchBaseError):
    pass


class ProgrammingError(SnowFinchBaseError):
    pass


class DatabaseError(SnowFinchBaseError):
    pass


class OperationalError(SnowFinchBaseError):
    pass


class ShellCommandException(RuntimeError):
    """Outputs proper logging when a ShellCommand fails"""
    pass


class CompressionError(SnowFinchBaseError):
    """
    Raised when there is an error compressing a file.
    """
    pass


class ClassNotFoundException(Exception):
    pass


class ConfigError(Exception):
    pass


class ParameterError(Exception):
    pass


class FieldTypeError(Exception):
    pass


class FieldNotExistsError(Exception):
    pass


class FieldAlreadyExistsError(Exception):
    pass


class FieldTypeValueConversionError(Exception):
    pass


class MigrationNotExistsError(Exception):
    pass


class MigrationNotCompatibleError(Exception):
    pass


class ResourceNotExistsError(Exception):
    pass


class TableNotExistsError(Exception):
    pass


class DBError(Exception):
    """
    Base class for all DBSource errors.
    """


class CredentialsError(DBError):
    """
    Raised when the users credentials are not provided.
    """


class S3Error(Exception):
    """
    Base class for all S3 errors.
    """


class S3CredentialsError(S3Error):
    """
    Raised when there is an error with AWS credentials.
    """


class S3InitializationError(S3Error):
    """
    Raised when there is an error initializing S3 client.
    """


class S3UploadError(S3Error):
    """
    Raised when there is an upload error to S3.
    """


class S3DownloadError(S3Error):
    """
    Raised when there is an download error to S3.
    """


class S3DeletionError(S3Error):
    """
    Raised when there is an deletion error on S3.
    """


class InvalidIdentifier(RuntimeError):
    """Python requires a specific format for its identifiers.
    https://docs.python.org/3.6/reference/lexical_analysis.html#identifiers
    """


def exceptions2exit(exception_list):
    """Decorator to convert given exceptions to exit messages
    This avoids displaying nasty stack traces to end-users
    Args:
        exception_list [Exception]: list of exceptions to convert
    """

    def exceptions2exit_decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except tuple(exception_list) as ex:
                from snowfinch.cli import get_log_level  # defer circular imports to avoid errors

                if get_log_level() <= logging.DEBUG:
                    # user surely wants to see the stacktrace
                    traceback.print_exc()
                print(f"ERROR: {ex}")
                sys.exit(1)

        return func_wrapper

    return exceptions2exit_decorator

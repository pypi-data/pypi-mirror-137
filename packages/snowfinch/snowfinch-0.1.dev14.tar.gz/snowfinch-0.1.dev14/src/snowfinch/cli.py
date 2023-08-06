"""
Command-Line-Interface(CLI) of SnowFinch
"""
import argparse
import confuse
from typing import List, Optional

from snowfinch import snowfinch_version
from snowfinch.parsers.parser import *
from snowfinch.aws.s3upload import *
from snowfinch.exceptions import *
from snowfinch.utils import regex
from snowfinch.shell import shell_command_error2exit_decorator


USAGE = (
    "\nTo see help text, you can run:\n"
    "  snowfinch help\n"
    "  snowfinch <command> help\n"
    "  snowfinch <command> <subcommand> help\n"
)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        usage=USAGE,
        description="Command Line Environment for SnowFinch.")

    # Required arguments
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Optional  argument
    optional.add_argument(
        "-v",
        "--version",
        action='version',
        version="snowfinch {ver}".format(ver=snowfinch_version),
        help="use this option to get SnowFinch latest version and exit",
    )
    required.add_argument(
        "-c",
        "--config",
        type=str,
        metavar='',
        required=True,
        help='use this option to read SnowFinch arguments from a given config file like .yaml, .yml, .ini, .toml',
    )

    optional.add_argument(
        '-s',
        '--secret',
        type=str,
        metavar='',
        help="use this option to handle sensitive configuration like DB Credentials, Secrete key etc")

    optional.add_argument(
        '-p',
        '--profile',
        type=str,
        metavar='',
        required=False,
        help='use this option to pick a specific environment configuration like dev, sit and prod',
    )

    required.add_argument(
        '-m',
        '--module',
        type=str,
        metavar='',
        required=True,
        help="use this option to run a specific SnowFinch module like bteq, ddl, s3 or all",
    )

    optional.add_argument(
        "-dt",
        "--drop-table",
        type=bool,
        default=False,
        metavar='',
        help='use this option if you want SnowFinch to drop and create tables',
    )

    required.add_argument(
        '-d',
        '--dialect',
        type=str,
        metavar='',
        required=True,
        help='use this option to select to select the dialect like mssql, teradata',
    )

    optional.add_argument(
        "-ll",
        "--log-level",
        type=str,
        metavar='',
        default="DEBUG",
        help="use this option to set the SnowFinch logging level to the desired verbosity",
    )

    optional.add_argument(
        '-cc',
        '--concurrency',
        metavar='',
        type=int,
        default=1,
        help="use this option to set the number of concurrent threads to use",
    )

    optional.add_argument(
        '-e',
        '--exclude',
        action='append',
        type=regex,
        metavar='',
        help="use this option to exclude a list of files using a regex method", )

    optional.add_argument(
        '-i',
        '--include',
        action='append',
        type=regex,
        metavar='',
        help="use this option to include list of files using a regex method",
    )

    parser.print_help()
    parser.print_usage()
    return parser.parse_args(args)


# def setup_logging(loglevel):
#     """Setup basic logger
#     Args:
#       loglevel (int): minimum loglevel for emitting messages
#     """
#     logformat = "%(asctime)s %(levelname)s:[%(name)s]:%(message)s"
#     logging.basicConfig(
#         level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
#     )


def main(args: List[str]):
    """
    Main entry point for external applications
        Args:
            args: command line arguments
    """
    args = parse_args(args)

    if args.concurrency < 1:
        logger.info("Concurrency must be positive.", file=sys.stderr)

    try:
        if args.log_level.upper() == "WARN":
            # logging.basicConfig(level=logging.WARN)
            logger.setLevel(level=logging.WARN)

        elif args.log_level.upper() == "INFO":
            # logging.basicConfig(level=logging.INFO)
            logger.setLevel(level=logging.INFO)
        elif args.log_level.upper()  == "DEBUG":
            # logging.basicConfig(level=logging.DEBUG)
            logger.setLevel(level=logging.DEBUG)

        logger.info("Log level set: {}".format(logger.getEffectiveLevel()))
    except ValueError:
        logger.error("Invalid log level: {}".format(args.verbose))
        sys.exit(1)

    # initiate the SnowFinch
    logger.info("Starting the SnowFinch Application...\n")

    # get the configs file
    app_config = args.config
    # profile = args.profile
    dialect = args.dialect

    if not os.path.isfile(app_config):
        print("File path {} does not exist. Exiting...".format(app_config))
        sys.exit()

    logger.info(f"Fetching application configs...")
    logger.info(f"application configs file: {app_config}")

    # initiate the configuration
    config = confuse.Configuration('SnowFinch', __name__)

    # Add conf items from specified file
    config.set_file(app_config)

    if args.module == 'bteq':
        logger.info("Running SnowFinch in bteq-only mode...\n")
        get_bteq_build(config)

    elif args.module == 'sproc':
        logger.info("Running SnowFinch in sproc-only mode...\n")
        get_sproc_build(dialect, config)

    elif args.module == 'ddl':
        logger.info("Running SnowFinch in ddl-only mode...\n")
        get_ddl_build(dialect, config, drop_table=args.drop_table)

    elif args.module == 's3':
        logger.info("Running SnowFinch in s3-only mode...\n")
        get_s3_upload(config)

    else:
        logger.info("Running SnowFinch full mode...\n")
        get_full_build(dialect, config, drop_table=args.drop_table)

    logger.info("SnowFinch executed successfully")


@shell_command_error2exit_decorator
@exceptions2exit([RuntimeError])
def run(args: Optional[List[str]] = None):
    """Entry point for console script"""
    print(f'Snowfinch Version: {snowfinch_version}')
    main(args or sys.argv[1:])


if __name__ == "__main__":
    main(sys.argv[1:])

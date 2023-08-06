import inspect
import logging
import os
import platform
from colorama import Fore
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Any, NoReturn, Union
from typing import Dict, List, Optional, Tuple

import pyfiglet
from colorama import Style

from snowfinch import snowfinch_version

LOG_ATTRIBUTES_TO_NAME_AND_FORMAT_AND_COLOR_DICT = {
    "asctime": ("s", Fore.YELLOW),
    "created": ("f", Fore.YELLOW),
    "msecs": ("d", Fore.YELLOW),
    "relativeCreated": ("d", Fore.YELLOW),
    "name": ("s", Fore.MAGENTA),
    "levelname": ("s", Fore.RED),
    "levelno": ("d", Fore.RED),
    "pathname": ("s", Fore.CYAN),
    "filename": ("s", Fore.CYAN),
    "lineno": ("d", Fore.CYAN),
    "module": ("s", Fore.BLUE),
    "funcName": ("s", Fore.BLUE),
    "process": ("d", Fore.LIGHTGREEN_EX),
    "processName": ("s", Fore.LIGHTGREEN_EX),
    "thread": ("d", Fore.LIGHTBLUE_EX),
    "threadName": ("s", Fore.LIGHTBLUE_EX),
    "exc_info": (None, Fore.BLACK),
    "exc_text": (None, Fore.BLACK),
    "stack_info": (None, Fore.BLACK),
    "args": (None, Fore.WHITE),
}
# "msg" and "message" are excluded on purpose

DEFAULT_IGNORE_ATTRIBUTE_LIST = [
    "args",
    "created",
    "exc_info",
    "exc_text",
    "pathname",
    "levelno",
    "msecs",
    "relativeCreated",
    "stack_info",
    "module",
    "funcName",
    "thread",
    "threadName",
    "process",
    "processName",
]


def get_apache_log_format(
        attr_config_dict: Dict[str, Tuple[Optional[str], Optional[str], int]],
        ignore_attr_list: List[str],
        add_colors: bool = False,
) -> str:
    format_list = list()
    for attr, (str_format, color) in attr_config_dict.items():

        if attr in ["message", "msg"] or attr in ignore_attr_list:
            continue

        # attr_name = attr if attr_name is None else attr_name
        str_format = "s" if str_format is None else str_format
        if add_colors is True:
            format_list.append(
                f"{Fore.LIGHTBLACK_EX}{Style.RESET_ALL} "
                + f"{color}%({attr}){str_format}{Style.RESET_ALL}:".strip()
            )
        else:
            format_list.append(f"%({attr}){str_format}")

    format_list.append("%(message)s")

    return " ".join(format_list)


class Apache(logging.Formatter):
    converter = datetime.fromtimestamp

    def __init__(self, fmt=None, datefmt=None, style="%", **kwargs):

        self.use_utc = kwargs.pop("use_utc", False)
        self.add_colors = kwargs.pop("add_colors", False)
        self.ignore_log_attribute_list = kwargs.pop("ignore_log_attribute_list", None)
        self.timezone = (
            timezone.utc if self.use_utc is True else datetime.now().astimezone().tzinfo
        )

        if self.ignore_log_attribute_list is None:
            self.ignore_log_attribute_list = DEFAULT_IGNORE_ATTRIBUTE_LIST

        if fmt is not None:
            log_format = fmt
        else:
            log_format: str = get_apache_log_format(
                attr_config_dict=LOG_ATTRIBUTES_TO_NAME_AND_FORMAT_AND_COLOR_DICT,
                ignore_attr_list=self.ignore_log_attribute_list,
                add_colors=self.add_colors,
            )
        super().__init__(fmt=log_format, datefmt=datefmt, style=style)

    def formatTime(self, record, datefmt=None):
        """Override: logger.Formatter.formatTime"""
        ct = self.converter(record.created)
        if datefmt is not None:
            s = ct.strftime(datefmt)
        else:
            s = datetime.fromtimestamp(record.created, tz=self.timezone)
        return s


class InvalidValue(Exception):
    def __init__(self, value: Any, allowed_value_list: List[Any]) -> NoReturn:
        self.value = value
        self.allowed_value_list = allowed_value_list

    def __str__(self) -> str:
        return f"'{self.value}' is not one of the allowed values: {self.allowed_value_list}."


class SnowFinchLogger(object):
    ALLOWED_FORMATTER_STR_LIST = ["json", "apache"]

    def __init__(
            self,
            project_name: str = "SnowFinch",
            log_level: str = "info",
            assign_logger_name: bool = False,
            formatter: Union[str, logging.Formatter] = "apache",
            log_to_stdout: bool = True,
            log_to_file: bool = False,
            log_dir: str = "logs",
            log_file_suffix: str = "S",
            rotate_file_by_size: bool = False,
            rotating_file_max_size_bytes: int = 1048576,
            rotate_file_by_time: bool = False,
            rotation_period: str = "H",
            rotation_interval: int = 1,
            rotation_time: datetime.time = None,
            rotating_file_backup_count: int = 1024,
            use_utc: bool = False,
            colors_to_stdout: bool = True,
            ignore_log_attribute_list: List[str] = None,
    ) -> NoReturn:

        self.project_name = project_name
        self.log_level = log_level.upper()
        self.assign_logger_name = assign_logger_name
        self.input_formatter = formatter
        self.log_to_stdout = log_to_stdout
        self.log_to_file = log_to_file
        self.log_dir = os.path.abspath(log_dir)
        self.log_file_suffix = log_file_suffix
        self.rotate_file_by_size = rotate_file_by_size
        self.rotating_file_max_size_bytes = rotating_file_max_size_bytes
        self.rotate_file_by_time = rotate_file_by_time
        self.rotation_period = rotation_period.upper()
        self.rotation_interval = rotation_interval
        self.rotation_time = rotation_time
        self.rotating_file_backup_count = rotating_file_backup_count
        self.use_utc = use_utc
        self.colors_to_stdout = colors_to_stdout
        self.ignore_log_attribute_list = ignore_log_attribute_list
        self.__set_logger()
        self.__set_log_handlers()
        self.__print_project_name()

    def __set_logger(self) -> NoReturn:
        if self.assign_logger_name is True:
            self.__logger = logging.getLogger(name=self.project_name)
        else:
            self.__logger = logging.getLogger()

        self.__logger.setLevel(self.log_level)

    def get_logger(self) -> logging.Logger:
        return self.__logger

    def __set_log_handlers(self) -> NoReturn:
        if self.rotate_file_by_size is True:
            self.__set_log_filepath(set_suffix=True)
            fh = RotatingFileHandler(
                filename=self.__log_filepath,
                encoding="utf-8",
                maxBytes=self.rotating_file_max_size_bytes,
                backupCount=self.rotating_file_backup_count,
            )
            self.__add_handler(handler=fh, add_colors=False)

        elif self.rotate_file_by_time is True:
            self.__validate_rotation_period()
            self.__set_log_filepath(set_suffix=False)
            fh = TimedRotatingFileHandler(
                filename=self.__log_filepath,
                encoding="utf-8",
                when=self.rotation_period,
                interval=self.rotation_interval,
                backupCount=self.rotating_file_backup_count,
                utc=self.use_utc,
                atTime=self.rotation_time,
            )
            self.__add_handler(handler=fh, add_colors=False)

        elif self.log_to_file is True:
            self.__set_log_filepath(set_suffix=True)
            fh = logging.FileHandler(filename=self.__log_filepath, encoding="utf-8")
            self.__add_handler(handler=fh, add_colors=False)

        else:
            pass

        if self.log_to_stdout is True:
            sh = logging.StreamHandler()
            self.__add_handler(handler=sh, add_colors=self.colors_to_stdout)

    def __set_log_filepath(self, set_suffix: bool = False) -> NoReturn:
        self.__set_log_filename(set_suffix=set_suffix)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.__log_filepath = os.path.join(self.log_dir, self.__log_filename)

    def __validate_rotation_period(self) -> NoReturn:
        allowed_rotation_period_list = ["S", "M", "H", "D", "MIDNIGHT"]
        allowed_rotation_period_list += list(map(lambda n: f"W{n}", range(0, 7)))
        if self.rotation_period not in allowed_rotation_period_list:
            raise InvalidValue(
                self.rotation_period,
                allowed_rotation_period_list,
            )

    def __set_log_filename(self, set_suffix: bool = False) -> NoReturn:
        if set_suffix is True:
            self.__log_filename = "{0}_{1}.{2}".format(
                self.project_name, self.__get_log_filename_suffix(), "log"
            )
        else:
            self.__log_filename = f"{self.project_name}.log"

    def __get_log_filename_suffix(self) -> str:
        suffix_to_date_time_format_dict = {
            "S": "%Y-%m-%d_%H-%M-%S",
            "M": "%Y-%m-%d_%H-%M-00",
            "H": "%Y-%m-%d_%H-00-00",
            "D": "%Y-%m-%d",
        }

        if self.log_file_suffix not in suffix_to_date_time_format_dict.keys():
            raise InvalidValue(
                self.log_file_suffix, list(suffix_to_date_time_format_dict.keys())
            )
        datetime_now = self.__get_datetime_now()

        return datetime_now.strftime(
            suffix_to_date_time_format_dict[self.log_file_suffix]
        )

    def __get_datetime_now(self) -> datetime:
        if self.use_utc is True:
            return datetime.utcnow()
        else:
            return datetime.now()

    def __add_handler(self, handler: logging.Handler, add_colors: bool) -> NoReturn:
        handler.setLevel(self.log_level)
        handler.setFormatter(self.__get_formatter(add_colors=add_colors))
        self.__logger.addHandler(handler)

    def __get_formatter(self, add_colors: bool) -> logging.Formatter:
        if isinstance(self.input_formatter, logging.Formatter) is True:
            return self.input_formatter

        elif isinstance(self.input_formatter, str) is True:
            # if self.input_formatter.lower() == "json":
            #     return Json(
            #         use_utc=self.use_utc,
            #         ignore_log_attribute_list=self.ignore_log_attribute_list,
            #     )
            if self.input_formatter.lower() == "apache":
                return Apache(
                    use_utc=self.use_utc,
                    add_colors=add_colors,
                    ignore_log_attribute_list=self.ignore_log_attribute_list,
                )
            else:
                raise InvalidValue(
                    value=self.input_formatter,
                    allowed_value_list=self.ALLOWED_FORMATTER_STR_LIST,
                )
        else:
            raise TypeError("'formatter' must be of type 'logger.Formatter' or 'str'")

    def __print_project_name(self) -> NoReturn:
        ascii_text = pyfiglet.figlet_format(self.project_name, font="slant")
        print(f"Welcome to\n{ascii_text}version {snowfinch_version}")
        print("Using Python version %s (%s, %s)" % (
            platform.python_version(),
            platform.python_build()[0],
            platform.python_build()[1]))
        print("Supported dialects: 'Teradata', 'Microsoft SQL Server', 'SnowFlake'.")

    def log_function_call(self, func):
        def wrapper(*args, **kwargs):
            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            self.get_logger().info(
                "{0}.{1}({2})".format(
                    func.__module__,
                    func.__qualname__,
                    ", ".join("{} = {!r}".format(*item) for item in func_args.items()),
                )
            )
            return func(*args, **kwargs)

        return wrapper


log = SnowFinchLogger(
    project_name="SnowFinch",
    log_to_stdout=False,
    formatter="apache",
    log_to_file=True,
    log_dir="/Users/ag29266/Downloads/snowfinch/logs"
)

# package
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

snowfinch_version = __version__
__author__ = 'gangadhar kadam'

from __future__ import absolute_import

import os
import ntpath
import errno
from typing import List
import re


def file_exists(path):
    try:
        with open(path):
            return True
    except (OSError, IOError):
        return False


def file_permissions(path):
    return os.stat(path).st_mode & 0o777


def home_file(filename):
    return os.path.join(os.path.expanduser("~"), filename)


def isfile(s):
    if isinstance(s, (str, bytes)) and ' ' not in s and file_exists(s):
        return True
    return False


def is_source(filename):
    suffixes = ('.sh', '.hql', '.sql', '.txt')
    for s in suffixes:
        if filename.endswith(s):
            return True
    return False


def get_outfile_name(infile, extension):
    filename = ntpath.basename(infile)
    out_file_name = filename.split(".")[0] + extension
    return out_file_name


def get_outfile_full_name(infile, extension):
    filename = ntpath.basename(infile)
    filepath = ntpath.dirname(infile)
    out_file_name = filename.split(".")[0]
    outfilename = f"{filepath}/{out_file_name}.{ extension}"
    return outfilename


def silent_remove(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:  # no such file or directory
            raise  # re-raise exception if a different error occurred


def get_version_info():
    from snowfinch.__init__ import __version__
    return __version__


def import_string(import_name):
    import_name = str(import_name)
    if not import_name.startswith("snowfinch."):
        import_name = "snowfinch.{}".format(import_name)
    try:
        return __import__(import_name)
    except ImportError:
        try:
            module_name, obj_name = import_name.rsplit('.', 1)
        except AttributeError as error:
            raise ImportError(error)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            module = import_string(module_name)
        try:
            return getattr(module, obj_name)
        except AttributeError as error:
            raise ImportError(error)


def regex(value):
    """ Helper for regex types on the command line. """
    try:
        return re.compile(value)
    except Exception as ex:
        print(ex)
        raise ValueError


def get_file_paths_list(local_dir: str) -> List[str]:
    """
    Create list of file paths.
    :param local_dir: Local filepath of assets to SCP to host.
    :type local_dir: List[str]
    """
    local_files = os.walk(local_dir)
    for root, dirs, files in local_files:
        return [f"{local_dir}/{file}" for file in files]

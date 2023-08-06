"""Legacy :mod:`os` module."""
from __future__ import absolute_import

# Add temporary imports.
import sys as __sys

# Import `os` members.
from os import *
from os import __all__
from os import __doc__
__all__ = list(__all__)

# Start with backports.
if __sys.version_info[:2] < (3, 2):

    # Backport info:
    # - Python 3.2: first appeareance.
    # pylint: disable=redefined-outer-name
    def makedirs(name, mode=0o777, exist_ok=False):
        """makedirs(name [, mode=0o777][, exist_ok=False])

        Super-mkdir; create a leaf directory and all intermediate ones.  Works like
        mkdir, except that any intermediate path segment (not just the rightmost)
        will be created if it does not exist. If the target directory already
        exists, raise an OSError if exist_ok is False. Otherwise no exception is
        raised.  This is recursive.
        """

        import os
        import errno

        exist_ok = bool(exist_ok)
        try:
            os.makedirs(name, mode)
        except OSError as err:
            if exist_ok and os.path.isdir(name) and err.errno == errno.EEXIST:
                return
            raise

    if "makedirs" not in __all__:
        __all__.append("makedirs")

if (3, 3) <= __sys.version_info[:2] < (3, 5):

    # Backport info:
    # - Python 3.3: several `os` functions were removed from `__all__`.
    # - Python 3.5: former `os` functions were brought back to `__all__`.
    # pylint: disable=redefined-outer-name,no-name-in-module,unused-import
    from os import abort
    from os import access
    from os import chdir
    from os import chmod
    from os import chown
    from os import chroot
    from os import close
    from os import closerange
    from os import confstr
    from os import confstr_names
    from os import ctermid
    from os import device_encoding
    from os import dup
    from os import dup2
    from os import environ
    from os import error
    from os import execv
    from os import execve
    from os import fchdir
    from os import fchmod
    from os import fchown
    from os import fdatasync
    from os import fork
    from os import forkpty
    from os import fpathconf
    from os import fstat
    from os import fstatvfs
    from os import fsync
    from os import ftruncate
    from os import get_terminal_size
    from os import getcwd
    from os import getcwdb
    from os import getegid
    from os import geteuid
    from os import getgid
    from os import getgrouplist
    from os import getgroups
    from os import getloadavg
    from os import getlogin
    from os import getpgid
    from os import getpgrp
    from os import getpid
    from os import getppid
    from os import getpriority
    from os import getresgid
    from os import getresuid
    from os import getsid
    from os import getuid
    from os import getxattr
    from os import initgroups
    from os import isatty
    from os import kill
    from os import killpg
    from os import lchown
    from os import link
    from os import listdir
    from os import listxattr
    from os import lockf
    from os import lseek
    from os import lstat
    from os import major
    from os import makedev
    from os import minor
    from os import mkdir
    from os import mkfifo
    from os import mknod
    from os import nice
    from os import open
    from os import openpty
    from os import pathconf
    from os import pathconf_names
    from os import pipe
    from os import posix_fadvise
    from os import posix_fallocate
    from os import pread
    from os import pwrite
    from os import read
    from os import readlink
    from os import readv
    from os import remove
    from os import removexattr
    from os import rename
    from os import replace
    from os import rmdir
    from os import sched_get_priority_max
    from os import sched_get_priority_min
    from os import sched_getaffinity
    from os import sched_getparam
    from os import sched_getscheduler
    from os import sched_param
    from os import sched_rr_get_interval
    from os import sched_setaffinity
    from os import sched_setparam
    from os import sched_setscheduler
    from os import sched_yield
    from os import sendfile
    from os import setegid
    from os import seteuid
    from os import setgid
    from os import setgroups
    from os import setpgid
    from os import setpgrp
    from os import setpriority
    from os import setregid
    from os import setresgid
    from os import setresuid
    from os import setreuid
    from os import setsid
    from os import setuid
    from os import setxattr
    from os import stat
    from os import stat_float_times
    from os import stat_result
    from os import statvfs
    from os import statvfs_result
    from os import strerror
    from os import symlink
    from os import sync
    from os import sysconf
    from os import sysconf_names
    from os import system
    from os import tcgetpgrp
    from os import tcsetpgrp
    from os import terminal_size
    from os import times
    from os import times_result
    from os import truncate
    from os import ttyname
    from os import umask
    from os import uname
    from os import uname_result
    from os import unlink
    from os import urandom
    from os import utime
    from os import wait
    from os import wait3
    from os import wait4
    from os import waitid
    from os import waitid_result
    from os import waitpid
    from os import write
    from os import writev
    __all__.extend([
        "abort", "access", "chdir", "chmod", "chown", "chroot", "close",
        "closerange", "confstr", "confstr_names", "ctermid",
        "device_encoding", "dup", "dup2", "environ", "error", "execv",
        "execve", "fchdir", "fchmod", "fchown", "fdatasync", "fork",
        "forkpty", "fpathconf", "fstat", "fstatvfs", "fsync", "ftruncate",
        "get_terminal_size", "getcwd", "getcwdb", "getegid", "geteuid",
        "getgid", "getgrouplist", "getgroups", "getloadavg", "getlogin",
        "getpgid", "getpgrp", "getpid", "getppid", "getpriority",
        "getresgid", "getresuid", "getsid", "getuid", "getxattr",
        "initgroups", "isatty", "kill", "killpg", "lchown", "link",
        "listdir", "listxattr", "lockf", "lseek", "lstat", "major",
        "makedev", "minor", "mkdir", "mkfifo", "mknod", "nice", "open",
        "openpty", "pathconf", "pathconf_names", "pipe", "posix_fadvise",
        "posix_fallocate", "pread", "pwrite", "read", "readlink", "readv",
        "remove", "removexattr", "rename", "replace", "rmdir",
        "sched_get_priority_max", "sched_get_priority_min",
        "sched_getaffinity", "sched_getparam", "sched_getscheduler",
        "sched_param", "sched_rr_get_interval", "sched_setaffinity",
        "sched_setparam", "sched_setscheduler", "sched_yield", "sendfile",
        "setegid", "seteuid", "setgid", "setgroups", "setpgid", "setpgrp",
        "setpriority", "setregid", "setresgid", "setresuid", "setreuid",
        "setsid", "setuid", "setxattr", "stat", "stat_float_times",
        "stat_result", "statvfs", "statvfs_result", "strerror", "symlink",
        "sync", "sysconf", "sysconf_names", "system", "tcgetpgrp",
        "tcsetpgrp", "terminal_size", "times", "times_result", "truncate",
        "ttyname", "umask", "uname", "uname_result", "unlink", "urandom",
        "utime", "wait", "wait3", "wait4", "waitid", "waitid_result",
        "waitpid", "write", "writev"])

# Remove temporary imports.
del __sys

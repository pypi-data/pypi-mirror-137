"""Tests for :mod:`pylegacy.os`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyLegacyOs(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.os`."""

    def setUp(self):
        """Define the test scope variables."""

        self.os_missing_attrs = [
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
            "waitpid", "write", "writev"]

    @unittest.skipIf(not (3, 3) <= sys.version_info[:2] < (3, 5), reason="no fix needed")
    def test_os_missing_attributes_available(self):
        """Test that :mod:`os` attributes are present in Python 3.3 and 3.4."""

        from pylegacy import os
        for attr in self.os_missing_attrs:
            self.assertTrue(hasattr(os, attr))

    @unittest.skipIf(sys.version_info[:2] >= (3, 2), reason="it has exist_ok")
    def test_os_makedirs_error_args(self):
        """Test that :func:`os.makedirs` does not have `exist_ok` arg."""

        import os
        self.assertRaises(TypeError, os.makedirs, "dummy", 511, True)

    @unittest.skipIf(sys.version_info[:2] >= (3, 2), reason="it has exist_ok")
    def test_os_makedirs_error_kwargs(self):
        """Test that :func:`os.makedirs` does not have `exist_ok` kwarg."""

        import os
        self.assertRaises(TypeError, os.makedirs, "dummy", exist_ok=True)

    def test_pylegacy_os_makedirs(self):
        """Test usage of :func:`pylegacy.os.makedirs`."""

        import shutil
        import tempfile
        from pylegacy import os

        tmpdir = tempfile.mkdtemp()
        testdir = os.path.join(tmpdir, "dummy", "folder")

        try:
            # Test that the dummy folder does not exist.
            self.assertFalse(os.path.isdir(testdir))
            # Test creation of dummy folder.
            ret = os.makedirs(testdir)
            self.assertIs(ret, None)
            self.assertTrue(os.path.isdir(testdir))
            # Test `makedirs` raising error with `exist_ok` not set.
            self.assertRaises(OSError, os.makedirs, testdir)
            # Test `makedirs` raising error with `exist_ok` set to False.
            self.assertRaises(OSError, os.makedirs, testdir, exist_ok=False)
            # Test `makedirs` skipping error with `exist_ok` set to True.
            ret = os.makedirs(testdir, exist_ok=True)
            self.assertIs(ret, None)
        finally:
            shutil.rmtree(tmpdir)


if __name__ == "__main__":
    unittest.main()

"""Tests for :mod:`pylegacy.tempfile`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyLegacyTempfile(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.tempfile`."""

    def setUp(self):
        """Define the test scope variables."""

    @unittest.skipIf(sys.version_info[:2] >= (3, 2), reason="it exists")
    def test_temporarydirectory_missing(self):
        """Test that :class:`~tempfile.TemporaryDirectory` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=no-name-in-module
            from tempfile import TemporaryDirectory
            return TemporaryDirectory

        self.assertRaises(ImportError, test_callable)

    def test_pylegacy_temporarydirectory_available(self):
        """Test use case of legacy :class:`~pylegacy.tempfile.TemporaryDirectory`."""

        from pylegacy import os
        from pylegacy.tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmpdir:
            tmpname = tmpdir
            self.assertTrue(isinstance(tmpdir, str))
            self.assertTrue(os.path.exists(tmpname))
            self.assertTrue(os.path.isdir(tmpname))
        self.assertFalse(os.path.exists(tmpname))

    def test_pylegacy_temporarydirectory_finalize(self):
        """Test removal of :class:`~pylegacy.tempfile.TemporaryDirectory` reference."""

        from pylegacy import os
        from pylegacy.builtins import ResourceWarning
        from pylegacy.tempfile import TemporaryDirectory

        tmpdir = TemporaryDirectory()  # pylint: disable=refactoring
        self.assertTrue(isinstance(tmpdir, TemporaryDirectory))
        self.assertTrue(os.path.exists(tmpdir.name))
        self.assertTrue(os.path.isdir(tmpdir.name))

        with self.assertWarns(ResourceWarning):
            # pylint: disable=protected-access
            tmpdir._finalizer()
        self.assertFalse(os.path.exists(tmpdir.name))


if __name__ == "__main__":
    unittest.main()

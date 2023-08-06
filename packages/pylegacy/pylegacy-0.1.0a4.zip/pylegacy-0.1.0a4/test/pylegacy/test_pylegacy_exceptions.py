"""Tests for :mod:`pylegacy.exceptions`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyLegacyExceptions(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.exceptions`."""

    def setUp(self):
        """Define the test scope variables."""

    def test_exceptions_availability(self):
        """Test availability of :mod:`pylegacy.exceptions` for Py2 or Py3."""

        def test_callable1():
            """Helper function 1."""
            import pylegacy.exceptions
            return isinstance(pylegacy.exceptions, object)

        def test_callable2():
            """Helper function 2."""
            from pylegacy import exceptions
            return isinstance(exceptions, object)

        if sys.version_info[:1] < (3,):
            self.assertTrue(test_callable1())
            self.assertTrue(test_callable2())
        else:
            self.assertRaises(ImportError, test_callable1)
            self.assertRaises(ImportError, test_callable2)

    @unittest.skipIf(sys.version_info[:1] >= (3,), reason="it exists")
    def test_pylegacy_resourcewarning_available(self):
        """Test that :class:`ResourceWarning` exists with :mod:`pylegacy`."""

        import warnings
        from pylegacy.exceptions import ResourceWarning

        with self.assertWarns(ResourceWarning):
            warnings.warn("this is a ResourceWarning message", ResourceWarning)


if __name__ == "__main__":
    unittest.main()

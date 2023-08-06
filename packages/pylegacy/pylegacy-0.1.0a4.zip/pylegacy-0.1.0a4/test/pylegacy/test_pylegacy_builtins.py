"""Tests for :mod:`pylegacy.builtins`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyLegacyBuiltins(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.builtins`."""

    def setUp(self):
        """Define the test scope variables."""

    @unittest.skipIf(sys.version_info[:2] < (3, 0), reason="it exists")
    @unittest.skipIf(sys.version_info[:2] >= (3, 2), reason="it exists")
    def test_callable_missing(self):
        """Test that :class:`callable` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=undefined-variable
            return callable  # noqa: F821

        self.assertRaises(NameError, test_callable)

    def test_pylegacy_callable_available(self):
        """Test that :class:`pylegacy.builtins.callable` is available."""

        from pylegacy.builtins import callable

        self.assertTrue(callable(int))
        self.assertFalse(callable(1))

    @unittest.skipIf(sys.version_info[:2] >= (3, 2), reason="it exists")
    def test_resourcewarning_missing(self):
        """Test that :class:`ResourceWarning` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=undefined-variable
            return ResourceWarning  # noqa: F821

        self.assertRaises(NameError, test_callable)

    def test_pylegacy_resourcewarning_available(self):
        """Test that :class:`ResourceWarning` exists with :mod:`pylegacy`."""

        import warnings
        from pylegacy.builtins import ResourceWarning

        with self.assertWarns(ResourceWarning):
            warnings.warn("this is a ResourceWarning message", ResourceWarning)


if __name__ == "__main__":
    unittest.main()

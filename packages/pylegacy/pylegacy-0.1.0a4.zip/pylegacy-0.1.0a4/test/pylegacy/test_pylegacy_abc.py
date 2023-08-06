"""Tests for :mod:`pylegacy.abc`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyLegacyAbc(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.abc`."""

    def setUp(self):
        """Define the test scope variables."""

    @unittest.skipIf(sys.version_info[:2] >= (3, 4), reason="it exists")
    def test_abc_missing(self):
        """Test that :class:`abc.ABC` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=no-name-in-module
            from abc import ABC
            return ABC

        self.assertRaises(ImportError, test_callable)

    def test_pylegacy_abc_available(self):
        """Test that :class:`pylegacy.abc.ABC` is available."""

        def test_callable():
            """Helper function."""
            from pylegacy.abc import ABC
            return ABC

        self.assertTrue(issubclass(test_callable(), object))


if __name__ == "__main__":
    unittest.main()

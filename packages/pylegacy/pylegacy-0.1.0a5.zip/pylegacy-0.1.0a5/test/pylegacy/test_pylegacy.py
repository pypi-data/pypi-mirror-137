"""Import test for :mod:`pylegacy`."""

import re
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyLegacy(unittest.TestCase):
    """Unittest class for :mod:`pylegacy`."""

    def setUp(self):
        """Define the test scope variables."""

    def test_import(self):
        """Test that basic library import is working."""

        import pylegacy

        regex = r"^(\d\.\d\.\d)(([abc]|rc)\d+)?(\+dev)?$"
        version = pylegacy.__version__
        self.assertTrue(isinstance(version, str))
        self.assertTrue(re.match(regex, version))


if __name__ == "__main__":
    unittest.main()

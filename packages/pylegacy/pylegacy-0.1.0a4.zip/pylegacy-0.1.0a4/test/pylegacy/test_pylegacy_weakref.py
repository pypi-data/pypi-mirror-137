"""Tests for :mod:`pylegacy.weakref`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyLegacyWeakref(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.weakref`."""

    def setUp(self):
        """Define the test scope variables."""

        from pylegacy.weakref import ref

        class Dummy(object):
            """Dummy class to test :mod:`pylegacy.weakref`."""

        self.obj = Dummy()
        self.ref = ref(self.obj)

    @unittest.skipIf(sys.version_info[:2] >= (3, 4), reason="it exists")
    def test_finalize_missing(self):
        """Test that :class:`weakref.finalize` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=no-name-in-module
            from weakref import finalize
            return finalize

        self.assertRaises(ImportError, test_callable)

    def test_finalize_available(self):
        """Test that :class:`pylegacy.weakref.finalize` is available."""

        def test_callable():
            """Helper function."""
            from pylegacy.weakref import finalize
            return finalize

        self.assertTrue(issubclass(test_callable(), object))

    def test_finalize_alive(self):
        """Test `alive` property in :class:`pylegacy.weakref.finalize`."""

        from pylegacy.weakref import finalize

        objfin = finalize(self.obj, lambda name, warn_message: None, "dummy",
                          warn_message="Implicitly cleaning")

        self.assertTrue(objfin.alive)

    def test_finalize_atexit(self):
        """Test `atexit` property in :class:`pylegacy.weakref.finalize`."""

        from pylegacy.weakref import finalize

        objfin = finalize(self.obj, lambda name, warn_message: None, "dummy",
                          warn_message="Implicitly cleaning")

        self.assertTrue(objfin.atexit)

    def test_finalize_atexit_setter(self):
        """Test `atexit` property setter in :class:`pylegacy.weakref.finalize`."""

        from pylegacy.weakref import finalize

        objfin = finalize(self.obj, lambda name, warn_message: None, "dummy",
                          warn_message="Implicitly cleaning")

        objfin.atexit = False
        self.assertFalse(objfin.atexit)

    def test_finalize_call(self):
        """Test call to :class:`pylegacy.weakref.finalize`."""

        from pylegacy.weakref import finalize

        objfin = finalize(self.obj, lambda name, warn_message: "bye", "dummy",
                          warn_message="Implicitly cleaning")

        result = objfin()
        self.assertEqual(result, "bye")

        result = objfin()
        self.assertIs(result, None)

    def test_finalize_detach(self):
        """Test `detach` method in :class:`pylegacy.weakref.finalize`."""

        from pylegacy.weakref import finalize

        objfin = finalize(self.obj, lambda name, warn_message: "bye", "dummy",
                          warn_message="Implicitly cleaning")

        result = objfin.detach()
        self.assertIsNot(result, None)

        result = objfin.detach()
        self.assertIs(result, None)

    def test_finalize_peek(self):
        """Test `peek` method in :class:`pylegacy.weakref.finalize`."""

        from pylegacy.weakref import finalize

        objfin = finalize(self.obj, lambda name, warn_message: "bye", "dummy",
                          warn_message="Implicitly cleaning")

        result = objfin.peek()
        self.assertIsNot(result, None)

        objfin()
        result = objfin.peek()
        self.assertIs(result, None)


if __name__ == "__main__":
    unittest.main()

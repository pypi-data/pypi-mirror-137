"""Tests for :mod:`pylegacy.datetime`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


# pylint: disable=too-many-public-methods
class TestPyLegacyDatetime(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.datetime`."""

    def setUp(self):
        """Define the test scope variables."""

    @unittest.skipIf(sys.version_info[:2] >= (3, 2), reason="it exists")
    def test_timezone_missing(self):
        """Test that :class:`datetime.timezone` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=no-name-in-module
            from datetime import timezone
            return timezone

        self.assertRaises(ImportError, test_callable)

    def test_pylegacy_timezone_available(self):
        """Test that :class:`pylegacy.datetime.timezone` is available."""

        def test_callable():
            """Helper function."""
            from pylegacy.datetime import timezone
            return timezone

        self.assertTrue(issubclass(test_callable(), object))

    def test_pylegacy_timezone_init_invalid_offset_type(self):
        """Test creation of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        self.assertRaises(TypeError, dt.timezone, offset="dummy")

    def test_pylegacy_timezone_init_invalid_offset_negative(self):
        """Test creation of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=-25)
        self.assertRaises(ValueError, dt.timezone, offset)

    def test_pylegacy_timezone_init_invalid_offset_positive(self):
        """Test creation of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=+25)
        self.assertRaises(ValueError, dt.timezone, offset)

    def test_pylegacy_timezone_init_invalid_name_type(self):
        """Test creation of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        self.assertRaises(TypeError, dt.timezone, offset, name=0)

    def test_pylegacy_timezone_init(self):
        """Test creation of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertTrue(isinstance(tz, dt.timezone))

    def test_pylegacy_timezone_init_offset_using_seconds(self):
        """Test creation of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1, seconds=10)
        if sys.version_info[:2] < (3, 7):
            self.assertRaises(ValueError, dt.timezone, offset)
        else:
            tz = dt.timezone(offset)
            self.assertTrue(isinstance(tz, dt.timezone))

    def test_pylegacy_timezone_init_utc_giving_name(self):
        """Test creation of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=0)
        tz = dt.timezone(offset, name="UTC")

        self.assertIsNot(tz, dt.timezone.utc)

    def test_pylegacy_timezone_init_utc_not_giving_name(self):
        """Test creation of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=0)
        tz = dt.timezone(offset)

        self.assertIs(tz, dt.timezone.utc)

    def test_pylegacy_timezone_hash(self):
        """Test `hash` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertEqual(hash(tz), hash(tz.utcoffset(None)))

    def test_pylegacy_timezone_eq_true(self):
        """Test equality of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        tz1 = dt.timezone(offset=dt.timedelta(hours=1))
        tz2 = dt.timezone(offset=dt.timedelta(hours=1))

        self.assertTrue(tz1 == tz2)

    def test_pylegacy_timezone_eq_false_due_to_type(self):
        """Test equality of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        tz1 = dt.timezone(offset=dt.timedelta(hours=1))
        tz2 = "dummy"

        self.assertFalse(tz1 == tz2)

    def test_pylegacy_timezone_eq_false_due_to_value(self):
        """Test equality of :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        tz1 = dt.timezone(offset=dt.timedelta(hours=1))
        tz2 = dt.timezone(offset=dt.timedelta(hours=2))

        self.assertFalse(tz1 == tz2)

    def test_pylegacy_timezone_dst(self):
        """Test `dst` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertIs(tz.dst(None), None)

    def test_pylegacy_timezone_dst_invalid_dt(self):
        """Test `dst` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertRaises(TypeError, tz.dst, dt="dummy")

    def test_pylegacy_timezone_utcoffset(self):
        """Test `utcoffset` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertEqual(tz.utcoffset(None), offset)

    def test_pylegacy_timezone_utcoffset_invalid_dt(self):
        """Test `utcoffset` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertRaises(TypeError, tz.utcoffset, dt="dummy")

    def test_pylegacy_timezone_tzname_giving_name(self):
        """Test `tzname` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset, name="Berlin time")

        self.assertEqual(tz.tzname(None), "Berlin time")

    def test_pylegacy_timezone_tzname_not_giving_name_negative_offset(self):
        """Test `tzname` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=-2)
        tz = dt.timezone(offset)

        self.assertEqual(tz.tzname(None), "UTC-02:00")

    def test_pylegacy_timezone_tzname_not_giving_name_positive_offset(self):
        """Test `tzname` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=+5)
        tz = dt.timezone(offset)

        self.assertEqual(tz.tzname(None), "UTC+05:00")

    def test_pylegacy_timezone_tzname_invalid_dt(self):
        """Test `tzname` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertRaises(TypeError, tz.tzname, dt="dummy")

    def test_pylegacy_timezone_fromutc(self):
        """Test `fromutc` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)
        dtobj = dt.datetime(2000, 1, 1, tzinfo=tz)

        self.assertEqual(tz.fromutc(dtobj), dtobj + offset)

    def test_pylegacy_timezone_fromutc_invalid_type(self):
        """Test `fromutc` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertRaises(TypeError, tz.fromutc, "dummy")

    def test_pylegacy_timezone_fromutc_invalid_tzinfo_in_dt(self):
        """Test `fromutc` from :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)
        dtobj = dt.datetime(2000, 1, 1)

        self.assertRaises(ValueError, tz.fromutc, dtobj)

    def test_pylegacy_timezone_str(self):
        """Test `str` for :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=1)
        tz = dt.timezone(offset)

        self.assertEqual(str(tz), tz.tzname(None))

    def test_pylegacy_timezone_repr_utc(self):
        """Test `repr` for :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=0)
        tz = dt.timezone(offset)

        self.assertEqual(repr(tz), "datetime.timezone.utc")

    def test_pylegacy_timezone_repr_giving_name(self):
        """Test `repr` for :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=2)
        tz = dt.timezone(offset, name="Athens time")

        result = "datetime.timezone({0}, 'Athens time')".format(repr(offset))
        self.assertEqual(repr(tz), result)

    def test_pylegacy_timezone_repr_not_giving_name(self):
        """Test `repr` for :class:`pylegacy.datetime.timezone` objects."""

        from pylegacy import datetime as dt

        offset = dt.timedelta(hours=2)
        tz = dt.timezone(offset)

        result = "datetime.timezone({0})".format(repr(offset))
        self.assertEqual(repr(tz), result)

    def test_pylegacy_timezone_pickling_giving_name(self):
        """Test pickling :class:`pylegacy.datetime.timezone` objects."""

        import pickle
        from pylegacy import datetime as dt
        from pylegacy.tempfile import NamedTemporaryFile

        offset = dt.timedelta(hours=2)
        tz = dt.timezone(offset, name="Athens time")

        with NamedTemporaryFile(suffix=".pkl") as tmpfile:
            # Save to file.
            with open(tmpfile.name, "wb") as tmpfd:
                pickle.dump(tz, tmpfd)
            # Read file again.
            with open(tmpfile.name, "rb") as tmpfd:
                tzread = pickle.load(tmpfd)

        self.assertEqual(tzread, tz)

    def test_pylegacy_timezone_pickling_not_giving_name(self):
        """Test pickling :class:`pylegacy.datetime.timezone` objects."""

        import pickle
        from pylegacy import datetime as dt
        from pylegacy.tempfile import NamedTemporaryFile

        offset = dt.timedelta(hours=2)
        tz = dt.timezone(offset)

        with NamedTemporaryFile(suffix=".pkl") as tmpfile:
            # Save to file.
            with open(tmpfile.name, "wb") as tmpfd:
                pickle.dump(tz, tmpfd)
            # Read file again.
            with open(tmpfile.name, "rb") as tmpfd:
                tzread = pickle.load(tmpfd)

        self.assertEqual(tzread, tz)


if __name__ == "__main__":
    unittest.main()

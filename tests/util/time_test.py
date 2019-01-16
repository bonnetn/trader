# coding=utf-8
"""
Test package for time utility functions.
"""
from datetime import timedelta, datetime

from trader.util.time import convert_single_to_timedelta, convert_to_timedelta, remove_dates_in_past


class TestConvertSingleToTimedelta:
    """
    Test class for convert_single_to_timedelta.
    """

    # noinspection PyMissingOrEmptyDocstring
    def test_convert_single_to_timedelta_days(self):
        assert convert_single_to_timedelta("42j") == timedelta(days=42)

    # noinspection PyMissingOrEmptyDocstring
    def test_convert_single_to_timedelta_hours(self):
        assert convert_single_to_timedelta("42h") == timedelta(hours=42)

    # noinspection PyMissingOrEmptyDocstring
    def test_convert_single_to_timedelta_minutes(self):
        assert convert_single_to_timedelta("42m") == timedelta(minutes=42)

    # noinspection PyMissingOrEmptyDocstring
    def test_convert_single_to_timedelta_seconds(self):
        assert convert_single_to_timedelta("42s") == timedelta(seconds=42)


# noinspection PyMissingOrEmptyDocstring
def test_convert_to_timedelta():
    assert convert_to_timedelta("1j 2h 3m 5s") == timedelta(days=1, hours=2, minutes=3, seconds=5)


# noinspection PyMissingOrEmptyDocstring
def test_remove_dates_in_past():
    now = datetime.now()
    a = now + timedelta(hours=1)
    b = now - timedelta(hours=1)
    assert remove_dates_in_past({a, b}) == {a}

# def test_get_closest_datetime():
#    now = datetime.now()
#    a = now + timedelta(hours=1)
#    b = now + timedelta(hours=10)
#    c = now + timedelta(hours=20)
#    assert get_closest_datetime({a, b, c}) == a

"""
Time related utilitly functions.
"""
from datetime import timedelta, datetime
from typing import Set


def convert_single_to_timedelta(time_val):
    """
    Convert a string like "1h" or "1m" into a timedelta object.
    :param time_val: string
    :return: timedelta object
    """
    num = int(time_val[:-1])
    if time_val.endswith('s'):
        return timedelta(seconds=num)
    elif time_val.endswith('m'):
        return timedelta(minutes=num)
    elif time_val.endswith('h'):
        return timedelta(hours=num)
    elif time_val.endswith('j'):
        return timedelta(days=num)


def convert_to_timedelta(time_val):
    """
    Convert a string like "1h3m2s" into a timedelta object.
    :param time_val: string
    :return: timedelta object
    """
    time_val = time_val.split(" ")
    time = timedelta()
    for t in time_val:
        time += convert_single_to_timedelta(t)
    return time


def get_closest_datetime(ticks: Set[datetime]) -> timedelta:
    """
    Find the shortest timedelta between now and the provided datetimes.
    :param ticks: set of datetimes.
    :return: timedelta with the closest datetime
    """
    now = datetime.now()
    ticks = map(lambda x: x - now, ticks)
    ticks = list(ticks)
    ticks.sort()
    return ticks[0]


def remove_dates_in_past(ticks: Set[datetime]) -> Set[datetime]:
    """
    Get a set containing only datetimes in the future.
    :param ticks: set of datetimes
    :return: a set of datetimes
    """
    now = datetime.now()
    ticks = filter(lambda x: x > now, ticks)
    return set(ticks)

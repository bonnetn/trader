"""
Test package for config.
"""
from trader.util.config import parse_config


# noinspection PyMissingOrEmptyDocstring
def test_parse_config():
    usr, pwd, url = parse_config()
    assert usr
    assert pwd
    assert url

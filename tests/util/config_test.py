from trader.util.config import parse_config


def test_parse_config():
    usr, pwd, url = parse_config()
    assert usr
    assert pwd
    assert url

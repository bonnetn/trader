# coding=utf-8
"""
Configuration extraction package.
"""
import configparser

from trader.util.log import LOG


def parse_config():
    """
    Read config.ini to fetch the credentials of the user.
    :return: login, password and url
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    cred = config["credentials"]
    general = config["general"]
    url = general["url"].strip('"')

    LOG.debug("Loaded config.")
    return cred["login"], cred["password"], url

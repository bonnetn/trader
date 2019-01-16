# coding=utf-8
"""
Main package.
"""
from selenium import webdriver

from trader.bot import Bot
from trader.util.config import parse_config
from trader.util.log import LOG

if __name__ == "__main__":
    config = parse_config()
    LOG.info("Parsed the configuration file.")

    while True:
        # noinspection PyBroadException
        try:
            Bot(config, webdriver.Firefox).run()
        except Exception:
            LOG.exception("The bot crashed, restarting.")

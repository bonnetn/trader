# coding=utf-8
"""
Logging package.
"""
import logging

LOG = logging.getLogger("trader")
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)

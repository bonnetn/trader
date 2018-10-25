import logging

LOG = logging.getLogger("trader")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())

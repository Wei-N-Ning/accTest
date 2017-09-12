

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


def getLogger(moduleDotPath, *args, **kwargs):
    import logging
    return logging.getLogger(moduleDotPath)


def initialize(level=None):
    import logging
    logging.basicConfig()
    logging.root.setLevel(level if level is not None else INFO)

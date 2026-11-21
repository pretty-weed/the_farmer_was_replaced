import logger_obj
from __builtins__ import quick_print

_LEVEL_NAMES = {'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40, 'WARN': 30, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}

_internal_logger = quick_print
_use_stdlib = False

MAIN_LOGGER = "TFWR"
def _getLevelNamesMapping():
    return _LEVEL_NAMES
getLevelNamesMapping = _getLevelNamesMapping

_LEVEL_REVMAP = {}
for k in _LEVEL_NAMES:
    if _LEVEL_NAMES[k] not in _LEVEL_REVMAP:
        _LEVEL_REVMAP[_LEVEL_NAMES[k]] = k 

__all__ = ["LOGGER", "LOGGER_NAME", "setup_logging"]
LOGGER_NAME  = MAIN_LOGGER
LOG_LEVEL = getLevelNamesMapping()["DEBUG"]

def _getLogger(name:str = MAIN_LOGGER):
    return logger_obj

getLogger = _getLogger

def setup_logging(name: None):
    logger = getLogger(name or LOGGER_NAME)
    logger.setLevel(LOG_LEVEL)
    return logger


def use_stdlib(use: bool = True):
    global _use_stdlib
    global getLevelNamesMapping
    global getLogger
    global LOGGER_NAME
    global LOG_LEVEL
    _use_stdlib = use
    
    if use:
        from logging import getLevelNamesMapping, getLogger
        from os import getenv

        from stdlib_log_conf import basicConfig
        LOGGER_NAME = getenv("LOGGER_NAME", LOGGER_NAME)
        print(getenv("LOG_LEVEL", _LEVEL_REVMAP[LOG_LEVEL]))
        LOG_LEVEL = getLevelNamesMapping()[getenv("LOG_LEVEL", _LEVEL_REVMAP[LOG_LEVEL]).upper()]
        
        basicConfig(LOG_LEVEL)
    else:
        getLevelNamesMapping = _getLevelNamesMapping
        getLogger = _getLogger

    
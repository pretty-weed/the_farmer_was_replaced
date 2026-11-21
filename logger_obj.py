from __builtins__ import quick_print
from stdlib_patch import format

# Treat this module as an import so I can have a pseudo-logger in game

MAIN_LOGGER = "TFWR"
DISABLE_LOGGING = False

_LEVEL_NAMES = {'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40, 'WARN': 30, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
CRITICAL = _LEVEL_NAMES["CRITICAL"]
FATAL = _LEVEL_NAMES["FATAL"]
ERROR = _LEVEL_NAMES["ERROR"]
WARN = _LEVEL_NAMES["WARN"]
WARNING = _LEVEL_NAMES["WARNING"]
INFO = _LEVEL_NAMES["INFO"]
DEBUG = _LEVEL_NAMES["DEBUG"]

_LEVEL_REVMAP = {}
for k in _LEVEL_NAMES:
    if _LEVEL_NAMES[k] not in _LEVEL_REVMAP:
        _LEVEL_REVMAP[_LEVEL_NAMES[k]] = k 

__all__ = ["LOGGER", "LOGGER_NAME, LOG_LEVEL", "basicConfig", "setup_logging"]
LOGGER_NAME =  MAIN_LOGGER
LOG_LEVEL = "DEBUG"

# Treat this module as an import so I can have a pseudo-logger in game



def setLevel(level):
    global LOG_LEVEL
    LOG_LEVEL = level

def basicConfig(level=None):
    pass

def info(msg, a0=None, a1=None, a2=None, a3=None, a4=None, a5=None):
    if DISABLE_LOGGING:
        return
    _log(INFO, msg, a0, a1, a2, a3, a4, a5)
    

def debug(msg, a0=None, a1=None, a2=None, a3=None, a4=None, a5=None):

    if DISABLE_LOGGING:
        return
    _log(DEBUG, msg, a0, a1, a2, a3, a4, a5)

def warning(msg, a0=None, a1=None, a2=None, a3=None, a4=None, a5=None):

    if DISABLE_LOGGING:
        return
    _log(WARNING, msg, a0, a1, a2, a3, a4, a5)

def error(msg, a0=None, a1=None, a2=None, a3=None, a4=None, a5=None):
    if DISABLE_LOGGING:
        return
    _log(ERROR, msg, a0, a1, a2, a3, a4, a5)

def _log(level, msg, a0=None, a1=None, a2=None, a3=None, a4=None, a5=None):
    if DISABLE_LOGGING:
        return
    if level <= LOG_LEVEL:
        print()
        print("LOG LOG LOG")
        print()
        quick_print("[" + _LEVEL_REVMAP[level] + "]" + format(msg, a0, a1, a2, a3, a4, a5))

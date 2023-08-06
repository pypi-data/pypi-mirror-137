import os
import logging
from logging.handlers import RotatingFileHandler

log_fname = os.environ.get('logfile', 'logs/log')
_general_level = os.environ.get('godmode', 'info').upper()

_level = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}
_module_logger_config = {
    'logfile': 'debug',
}

formatter = logging.Formatter('[ %(levelname)s ]%(name)s: %(message)s')
file_formatter = logging.Formatter('%(asctime)s[ %(levelname)s ]%(name)s: %(message)s')


_sthandler = logging.StreamHandler()
_sthandler.setLevel(logging.DEBUG)
_sthandler.setFormatter(formatter)

# disabbling file logger karena error di cloud
# _fhandler = RotatingFileHandler(log_fname, mode="a", maxBytes=7485760, backupCount=5)
# _fhandler.setFormatter(file_formatter)
# _fhandler.setLevel(_level[_module_logger_config['logfile'].upper()])


def fullname(o):
    klass = o.__class__
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__ # avoid outputs like 'builtins.str'
    return module + '.' + klass.__qualname__


def create_logger(name, fname = None) -> logging.Logger:

    if not isinstance(name, str):
        name = fullname(name)

    if not fname:
        fname = log_fname

    logger = logging.getLogger(name)
    # print(logger.handlers, name)

    log_level = _module_logger_config.get(name, _general_level).upper()

    try:
        if(logger.hasHandlers()):
            logger.handlers.clear()
    except AttributeError as e:
        pass
        
    logger.propagate = False
    logger.setLevel(_level.get(log_level))

    # bagian file handlers
    # filehandler = _fhandler

    logger.addHandler(_sthandler)
    # logger.addHandler(filehandler)

    return logger
import logging
import sys
from logging import Formatter, StreamHandler, FileHandler


def setup_logging(level=logging.DEBUG, log_file='shell.log', console=True):
    """
    Сетапер логера

    Args:
        level (_type_, optional):Defaults to logging.DEBUG.
        log_file (str, optional):Defaults to 'shell.log'.
        console (bool, optional):Defaults to True.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    file_handler = FileHandler(log_file, encoding='utf-8', mode='w')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console:
        console_handler = StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


def get_logger(name):
    return logging.getLogger(name)

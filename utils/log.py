import logging
from settings import LOG_FILE_PATH

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)
logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def warning(msg, *args, **kwargs):
    logging.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logging.error(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logging.info(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    logging.critical(msg, *args, **kwargs)
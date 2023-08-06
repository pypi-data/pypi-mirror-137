import logging
import sys
from contextlib import ContextDecorator

LOGGER_NAME = "engine"


def create_logger():
    logger = logging.getLogger(LOGGER_NAME)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


logger = create_logger()


def set_log_level(level=logging.INFO):
    logging.getLogger(LOGGER_NAME).setLevel(level)


def set_no_logs():
    logging.getLogger(LOGGER_NAME).setLevel(sys.maxsize)


def set_info_logs():
    logging.getLogger(LOGGER_NAME).setLevel(logging.INFO)


def set_debug_logs():
    logging.getLogger(LOGGER_NAME).setLevel(logging.DEBUG)


class debug_engine_logs(ContextDecorator):
    def __enter__(self):
        self.previous_log_level = logger.level
        set_debug_logs()
        return self

    def __exit__(self, *exc):
        set_log_level(self.previous_log_level)
        return False


class info_engine_logs(ContextDecorator):
    def __enter__(self):
        self.previous_log_level = logger.level
        set_info_logs()
        return self

    def __exit__(self, *exc):
        set_log_level(self.previous_log_level)
        return False


class no_engine_logs(ContextDecorator):
    def __enter__(self):
        self.previous_log_level = logger.level
        set_no_logs()
        return self

    def __exit__(self, *exc):
        set_log_level(self.previous_log_level)
        return False

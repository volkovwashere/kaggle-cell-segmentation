import logging
from typing import Union


class CustomLogger:
    def __init__(self, logger=None):
        self.logger = logger

    @classmethod
    def construct_logger(cls, name: str, log_file_path: str, logger_level: Union[int, str],
                         formatter=logging.Formatter('%(levelname)s:%(name)s:%(message)s')):
        try:
            logger = logging.getLogger(name)
            logger.setLevel(logger_level)
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            return cls(logger)
        except FileNotFoundError:
            pass

    def log_info(self, message: str) -> None:
        self.logger.info(message)

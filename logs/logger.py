import logging
from logging.handlers import TimedRotatingFileHandler


def create_logger():
    logger = logging.getLogger("twitterflightbot")
    file_name = "logs/twitterflightbot.log"

    # Rotate logs daily and delete logs older than 7 days
    file_handler = TimedRotatingFileHandler(file_name, when="D", backupCount=7)
    formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger

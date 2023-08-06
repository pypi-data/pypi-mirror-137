from colorlog import ColoredFormatter
import logging

levels = ["critical", "error", "warning", "info", "debug"]
logging_levels = [logging.CRITICAL, logging.ERROR, logging.WARNING,
                  logging.INFO, logging.DEBUG]

# Based on https://stackoverflow.com/a/23964880/5107192
LOG_LEVEL = logging.DEBUG

logging.root.setLevel(LOG_LEVEL)

formatter = ColoredFormatter(
    "%(asctime)-15s %(log_color)s%(levelname)-8s [%(name)s] %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
handler.setFormatter(formatter)

logger = logging.getLogger('dlgsheet')
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)


def setLoggerLevel(level):

    if(level in levels):
        logger.setLevel(logging_levels[levels.index(level)])
    else:
        logger.warning("Not valid logging level: " +
                       level + ". Ignoring option.")

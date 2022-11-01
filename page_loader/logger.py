import logging
import os
LOG_FILE = 'page-loader.log'
LOGGER_PARAMS = {
    'info': logging.INFO,
    'warn': logging.WARNING,
    'debug': logging.DEBUG
}


def config_logger(param=logging.INFO):
    logging.basicConfig(
        level=LOGGER_PARAMS[param],
        format=u'%(levelname)-8s [%(asctime)s] %(message)s',
        filename=LOG_FILE)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.close()

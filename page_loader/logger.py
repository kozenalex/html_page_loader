import logging
import os.path
LOG_FILE = 'page-loader.log'

def config_logger(param=logging.INFO):
    logging.basicConfig(
        level=param,
        format = u'%(levelname)-8s [%(asctime)s] %(message)s',
        filename = LOG_FILE)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.close()
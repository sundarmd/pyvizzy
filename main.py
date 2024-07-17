import os
import logging
from pkg.server import start_server

def init_logging():
    log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
    try:
        logging_level = getattr(logging, log_level)
    except AttributeError:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    init_logging()
    start_server()
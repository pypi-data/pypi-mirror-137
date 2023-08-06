import logging
import traceback
import sys
from .speaker import Speaker

try:
    from .listener import Listener
except Exception:
    logging.debug(str(sys.exc_info()[0]))
    logging.debug(str(traceback.format_exc()))
    logging.error("Listener disabled due to missing libraries.")

try:
    from .watcher import Watcher
except Exception:
    logging.debug(str(sys.exc_info()[0]))
    logging.debug(str(traceback.format_exc()))
    logging.error("Watcher disabled due to missing libraries.")
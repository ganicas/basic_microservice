import logging
import os
from logging.handlers import TimedRotatingFileHandler

"""

    Logger main script. 
    Script will provide logging for all interfaces :
    INFO, WARN, ERROR, DEBUG

"""

basepath = os.path.dirname(__file__)
filepath_debug = os.path.abspath(os.path.join(basepath, "..", "..", "..", "..", "log/debug.log"))
filepath_info = os.path.abspath(os.path.join(basepath, "..", "..", "..", "..", "log/info.log"))
filepath_error = os.path.abspath(os.path.join(basepath, "..", "..", "..", "..", "log/error.log"))

########################################################################################################################

save_flask_files = os.path.abspath(
    os.path.join(basepath, "..", "..", "..", "ftp_files/history_files/download_history"))

export_csv_path = os.path.abspath(os.path.join(basepath, "..", "..", "..", "..", "exports/"))
export_email_path = os.path.abspath(
    os.path.join(basepath, "..", "..", "..",  "..", "email_exports/")
)

logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("application")

logger.setLevel(logging.DEBUG)
logger.propagate = False

sh = logging.StreamHandler()
sh.setLevel(logging.ERROR)

sh.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s CONSOLE %(message)s'))
logger.addHandler(sh)

# INFO LOGGER
fh_info = TimedRotatingFileHandler(filepath_info, backupCount=5)
fh_info.setLevel(logging.INFO)
fh_info.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s  %(message)s'))
logger.addHandler(fh_info)

# ERROR LOGGER
fh_error = TimedRotatingFileHandler(filepath_error, backupCount=5)
fh_error.setLevel(logging.ERROR)
fh_error.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
logger.addHandler(fh_error)

# DEBUG LOGGER
fh_debug = TimedRotatingFileHandler(filepath_debug, backupCount=5)
fh_debug.setLevel(logging.DEBUG)
fh_debug.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s  %(message)s'))
logger.addHandler(fh_debug)

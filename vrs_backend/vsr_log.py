import sys
import logging, os
from logging.handlers import RotatingFileHandler
from datetime import datetime
# from configparser import ConfigParser
# config = ConfigParser()
# config.read(os.path.join(setting.default_path,'config.ini'))
# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0

# hard coded filepath is specified but have to change when we deploy.
if not os.path.exists(os.path.join('/home/drivetech-sayali/Documents/DT_VSR', 'logs')):
    os.makedirs(os.path.join('/home/drivetech-sayali/Documents/DT_VSR', 'logs'))
handler = RotatingFileHandler(filename=os.path.join('/home/drivetech-sayali/Documents/DT_VSR/logs',f"DriveTech-{datetime.now().strftime('%Y-%m-%d %H_%M_%S')}.log"),mode='a', maxBytes=1024 * 1024 * 3, encoding=None,delay=False,backupCount=100)
# handler = RotatingFileHandler(filename=os.path.join(setting.log_dir,f"DriveTech-{datetime.now()}.log"), maxBytes=1024 * 1024)
# logging.basicConfig(filename=os.path.join(setting.log_dir,f"DriveTech-{datetime.now()}.log"), format = '%(asctime)s %(message)s', filemode='w')
formatter = logging.Formatter('%(asctime)s - %(message)s', "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter) 
logger = logging.getLogger(__name__)
logger.setLevel(20)
logger.addHandler(handler)
# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def vsrInfo(message):
    logger.info(message)

def vsrError(message):
    logger.error(message)

def vsrWarn(message):
    logger.warning(message)

def vsrDebug(message):
    logger.debug(message)

def vsrCritical(message):
    logger.critical(message)

def vsrException(message):
    logger.exception(message)

def vsrStartFunc(message):
    logger.info(f'+++ {message}')

def vsrEndFunc(message):
    logger.info(f'--- {message}')

def vsrQueryCompleted(message):
    logger.info(f'{message} query is executed successfully')

def vsrQueryRollback(message):
    logger.error(f'All queries related to {message} are rolled back')
    
def vsrQueryCommitted(message):
    logger.info(f'All queries related to {message} are committed successfully')

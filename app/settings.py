import logging
from os.path import isfile, dirname

import sentry_sdk
from envparse import env

# Init settings using the .env file
if isfile('.env'):
    env.read_envfile('.env')

SECRET_KEY = env.str('SECRET_KEY', default='')
DB_DSN = env.str('DB_DSN', default='')
BASE_DIR = dirname(dirname(__file__))

SENTRY_DSN = env.str('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(SENTRY_DSN)

formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "file": "%(filename)s", '
                              '"function": "%(funcName)s", "message": "%(message)s"}')
stream = logging.StreamHandler()
stream.setFormatter(formatter)

logger = logging.getLogger('crm')
logger.setLevel(logging.INFO)
logger.addHandler(stream)

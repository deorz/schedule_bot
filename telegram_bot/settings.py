import logging
import os
import sys

from dotenv import load_dotenv

from telegram_bot.messages import LOGGER_MESSAGES

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger_format = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(logger_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

TELEGRAM_TOKEN = os.getenv('Telegram_token')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
API_URL = os.getenv('API_url')
HOST = os.getenv('host')
USERNAME = os.getenv('user')
PASSWORD = os.getenv('password')
DB_NAME = os.getenv('db_name')
PORT = os.getenv('port')

variables = (TELEGRAM_TOKEN, HEROKU_APP_NAME, API_URL, HOST,
             USERNAME, PASSWORD, DB_NAME, PORT)

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TELEGRAM_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT'))


def variables_check():
    if not any(variables):
        logger.critical(LOGGER_MESSAGES['variables_error'])
        quit()

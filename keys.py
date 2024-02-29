import os

from dotenv import set_key

secret_key = os.environ.get('SECRET_KEY')
debug = os.environ.get('DEBUG')


set_key('.env', 'SECRET_KEY', secret_key)
set_key('.env', 'DEBUG', debug)


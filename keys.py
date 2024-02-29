import os

from dotenv import set_key

secret_key = os.environ.get('SECRET_KEY')
debug = os.environ.get('DEBUG')

db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')

set_key('.env', 'SECRET_KEY', secret_key)
set_key('.env', 'DEBUG', debug)

set_key('.env', 'DB_NAME', db_name)
set_key('.env', 'DB_USER', db_user)
set_key('.env', 'DB_PASSWORD', db_password)
set_key('.env', 'DB_HOST', db_host)

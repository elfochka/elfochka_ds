"""Модуль управления ключами приложения, для корректного запуска в Docker."""

import os

from dotenv import set_key

secret_key = os.environ.get('SECRET_KEY')
debug = os.environ.get('DEBUG')

stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')

set_key('.env', 'SECRET_KEY', secret_key)
set_key('.env', 'DEBUG', debug)

set_key('.env', 'STRIPE_PUBLIC_KEY', stripe_public_key)
set_key('.env', 'STRIPE_SECRET_KEY', stripe_secret_key)

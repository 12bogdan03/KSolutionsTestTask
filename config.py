import os
from decouple import config

CSRF_ENABLED = True

SECRET_KEY = config('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False

PAY_TRIO_SECRET_KEY = config('PAY_TRIO_SECRET_KEY')
PAY_TRIO_SHOP_ID = config('PAY_TRIO_SHOP_ID')

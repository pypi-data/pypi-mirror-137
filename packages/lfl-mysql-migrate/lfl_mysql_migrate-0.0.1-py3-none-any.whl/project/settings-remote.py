import os
from gettext import gettext

from isc_common.common import SFTP
from isc_common.ssh.ssh_client import SSH_Clients
from project import get_INSTALLED_APPS, get_MIDDLEWARE, get_TEMPLATES, get_AUTH_PASSWORD_VALIDATORS, get_STATICFILES_DIRS, get_LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR_DOCUMENT = '/home/lfl-old/'
OLD_SITE_BASE_DIR = 'C:\lflru\lflru\\'

FILES_STORE = dict(
    mode=SFTP,
    SSH_HOST='192.168.0.158',
    SSH_PORT=22,
    SSH_USER='download-image-content',
    SSH_PASSWORD='download-image-content',
    PATH='/home/download-image-content/images/FILES'
)

UNBOUNDED_FILES = '/home/download-image-content/images/UNBOUNDED_FILES'

SECRET_KEY = '3xy6k5wy51nbupqj$6n8=qmqrsc#ldos%=l9n#3z-4en@netwd'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = get_INSTALLED_APPS()

AUTH_USER_MODEL = 'isc_common.User'

MIDDLEWARE = get_MIDDLEWARE()

ROOT_URLCONF = 'project.urls'

TEMPLATES = get_TEMPLATES()

# DB_MYSQL_REM_HOST = '91.189.87.218'
DB_MYSQL_REM_HOST = '192.168.0.234'
DB_POSTGRES_HOST = '192.168.0.108'

WS_PORT = '8003'
WS_CHANNEL = 'common'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lfl-db',
        'USER': 'lfl-db',
        'PASSWORD': 'lfl-db',
        'HOST': DB_POSTGRES_HOST,
        'PORT': '5432',
    },
    'sitelfl': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lfl',
        'USER': 'lfl',
        'PASSWORD': '9B3{rQq?Gmls',
        'HOST': DB_MYSQL_REM_HOST,
        'PORT': '3306',
    },
}

AUTH_PASSWORD_VALIDATORS = get_AUTH_PASSWORD_VALIDATORS()

LANGUAGES = (
    ('ru-RU', gettext('Russian')),
    ('en', gettext('English')),
)

LANGUAGE_CODE = 'ru-RU'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TIME_ZONE = 'Europe/Moscow'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../static"))

STATICFILES_DIRS = get_STATICFILES_DIRS(BASE_DIR=BASE_DIR)

ASGI_APPLICATION = 'project.routing.application'

WSGI_APPLICATION = 'project.wsgi.application'

CHANNEL_LAYERS = {
    # 'default': {
    #     'BACKEND': 'channels_redis.core.RedisChannelLayer',
    #     'CONFIG': {
    #         'hosts': [('0', 6379)],
    #         'prefix': 'asgi-home',
    #         'expiry': 1,
    #         'capacity': 10000000,
    #     },
    # },
    'default': {
        'BACKEND': 'isc_common.ws.inMemoryChannelLayer.AsyncInMemoryChannelLayer',
    },
}

log_file_name = f'{BASE_DIR}{os.sep}logs{os.sep}debug.log'
log_file_name1 = f'{BASE_DIR}{os.sep}logs{os.sep}debug1.log'

with open(log_file_name, "w") as file:
    file.truncate()
with open(log_file_name1, "w") as file:
    file.truncate()

LOGGING = get_LOGGING(log_file_name=log_file_name, log_file_name1=log_file_name1)

DEFAULT_FILE_STORAGE = 'isc_common.storages.crypto_storage.CryptoFileSystemStorage'

REPLACE_FILE_PATH = {
    'C:/ivc': BASE_DIR_DOCUMENT,
    'c:/ivc': BASE_DIR_DOCUMENT
}

PATH_IMAGES_REPLACE = dict(
    old_path='C:\\lflru\\',
    new_path='/home/lfl-old/',
    tmp_path='/home/lfl-old/tmp',
)

REC_IMAGE = False

OLD_FILES = dict(
    SSH_HOST='192.168.0.219',
    SSH_USER='lfl-old',
    SSH_PASSWORD='lfl-old',
    SSH_PORT=22,
)

SSH_CLIENTS = SSH_Clients()

C_DUMPS_PATH = '/home/lfl-old-mysql/dumps-mysql'

MYSQL = "/usr/bin/mysql"
MYQL_DATABASE = "lfl"
MYQL_USERNAME = "lfl"
MYQL_PASSWORD = "9B3{rQq?Gmls"

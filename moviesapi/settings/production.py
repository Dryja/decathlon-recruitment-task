import os
import sentry_sdk
import dj_database_url
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

ALLOWED_HOSTS = [os.environ['SITE_URL']]
sentry_sdk.init(
    dsn=os.environ['SENTRY_KEY'], integrations=[DjangoIntegration()])

DATABASES = {}
DATABASES['default'] = dj_database_url.config(
    conn_max_age=500, ssl_require=True)

STATIC_URL = 'https://od.naprawszybko.pl/'  #static server for production

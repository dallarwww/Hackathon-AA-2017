# -*- coding: utf-8 -*-
import psycopg2 as psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import DictCursor

from backend import settings


DB_CONNECTION_TEMPLATE = "dbname='%s' host='%s' port='%s' user='%s' password='%s' application_name='%s'"
APPLICATION_NAME = "user_path_analysis"


def get_connection():
    db_name = "default"
    db_settings = settings.DATABASES[db_name]
    name = db_settings['NAME']
    host = db_settings['HOST']
    port = db_settings['PORT']
    user = db_settings['USER']
    password = db_settings['PASSWORD']

    conn = psycopg2.connect(DB_CONNECTION_TEMPLATE % (name, host, port, user, password, APPLICATION_NAME))
    if db_settings.get('OPTIONS', {}).get('autocommit', False):
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn
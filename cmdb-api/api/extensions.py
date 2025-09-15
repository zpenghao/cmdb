# -*- coding:utf-8 -*-


from celery import Celery
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from api.lib.secrets.inner import KeyManage
from api.lib.utils import ESHandler
from api.lib.utils import RedisHandler

bcrypt = Bcrypt()
babel = Babel()
login_manager = LoginManager()
db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate()
cache = Cache()
celery = Celery()
cors = CORS()
rd = RedisHandler()
es = ESHandler()
inner_secrets = KeyManage()

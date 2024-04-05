from decouple import config

DATABASE_URI = config("DATABASE_URL",default="sqlite:///bac.sqlite")
if DATABASE_URI.startswith("postgres://"):
    DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)

class Config(object):
  DEBUG = False
  TESTING = False
  SQLALCHEMY_DATABASE_URI = DATABASE_URI
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  BCRYPT_LOG_ROUNDS = 13
  WTF_CSRF_ENABLED = True
  DEBUG_TB_ENABLED = False
  DEBUG_TB_INTERCEPT_REDIRECTS = False
  SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT", default="very-important")
  # Mail Settings
  MAIL_DEFAULT_SENDER="noreply@bac.com"
  MAIL_SERVER = "smtp.gmail.com"
  MAIL_PORT= 465
  MAIL_USE_TLS = False
  MAIL_USE_SSL = True
  MAIL_DEBUG = False
  MAIL_USERNAME = "bac.chu.dijon@gmail.com" #config("EMAIL_USER")
  MAIL_PASSWORD = "pirl pcym adbu yvuu" #config("EMAIL_PASSWORD")


class DevelopmentConfig(Config):
  SECRET_KEY='dev'
  DEVELOPMENT = True
  DEBUG = True
  WTF_CSRF_ENABLED = False
  DEBUG_TB_ENABLED = True

class TestingConfig(Config):
  TESTING = True
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"

class ProductionConfig(Config):
  DEBUG = False
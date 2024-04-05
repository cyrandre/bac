import os
from flask import Flask
from .config import DevelopmentConfig,ProductionConfig,Config

def create_app(config=None):
  # Create and configure the app
  app = Flask(__name__,instance_relative_config=True)

  app.config.from_mapping(    
    UPLOAD_FOLDER= os.path.join(app.static_folder,'images')
  )

  # Load configuration
  if config is None:
    if app.config['DEBUG']:
      obj = DevelopmentConfig
    else:
      obj = ProductionConfig      
    app.config.from_object(obj)
  elif isinstance(config,Config):
    app.config.from_object(config)
  else:
    app.config.from_mapping(config)
  
  # Ensure the instance folder exists
  try:
      os.makedirs(app.instance_path)
  except OSError:
      pass
  
  # Ensure the upload folder exists
  try:
     os.makedirs(app.config['UPLOAD_FOLDER'])
  except OSError:
     pass
  
  # Loggin Manager
  from .plugins.login import login_manager,create_admin
  login_manager.init_app(app)
  login_manager.login_view = "accounts.login"
  login_manager.login_message_category = "danger"
  app.cli.add_command(create_admin)

  # Init mail
  from .plugins.email import mail
  mail.init_app(app)
  
  # Init db
  from .plugins.models import db,migrate,bcrypt,load_questions
  db.init_app(app)
  migrate.init_app(app,db)
  bcrypt.init_app(app)
  app.cli.add_command(load_questions)

  from .views import accounts,session,admin
  app.register_blueprint(accounts.bp)
  app.register_blueprint(session.bp)
  app.register_blueprint(admin.bp)
  
  app.add_url_rule('/', endpoint='index')

  return app
#src/app.py

from flask import Flask

from .config import app_config
from .infraestructure.repository.mysql import db, bcrypt

# import user_api blueprint
from .interface.rest.home_controller import home_api


def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(home_api, url_prefix='/v1/book-house')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Welcome to Python Flask Microservice API'

  return app


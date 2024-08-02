from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from task_manager1.app1.db import db
from task_manager1.app1.config import Config
from task_manager1.app1.db import db
from task_manager1.app1.resources.user import UserRegister, UserLogin
from task_manager1.app1.resources.task import TaskResource, TaskList, TaskAssign
# app = Flask(__name__)
# app.config.from_object('task_manager1.app.config.Config')
#
# db.init_app(app)
# jwt = JWTManager(app)
# from task_manager1.app import models, resources
#
#

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object('task_manager1.app1.config.TestingConfig')
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)


    with app.app_context():
        db.create_all()

    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(TaskResource, '/task/<int:task_id>')
    api.add_resource(TaskList, '/tasks')
    api.add_resource(TaskAssign, '/task/<int:task_id>/assign')

    return app




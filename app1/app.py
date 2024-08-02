from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
# from task_manager1.app.config import Config
# from task_manager1.app.db import db
# from task_manager1.app.resources.user import UserRegister, UserLogin
# from task_manager1.app.resources.task import TaskResource, TaskList, TaskAssign
from .config import Config
from .db import db
from .resources.user import UserRegister, UserLogin
from .resources.task import TaskResource, TaskList, TaskAssign
app = Flask(__name__)
app.config.from_object('task_manager1.app1.config.TestingConfig')
api = Api(app)
jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TaskResource, '/task/<int:task_id>')
api.add_resource(TaskList, '/tasks')
api.add_resource(TaskAssign, '/task/<int:task_id>/assign')


if __name__ == '__main__':
    app.run(debug=True)
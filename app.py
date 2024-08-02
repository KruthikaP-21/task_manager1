from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app1.config import Config
from app1.db import db
from app1.resources.user import UserRegister, UserLogin
from app1.resources.task import TaskResource, TaskList, TaskAssign

app = Flask(__name__)
app.config.from_object(Config)
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


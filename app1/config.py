import os

class Config:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Krutu%402001@localhost/task_manager1'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db')
    # SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    JWT_SECRET_KEY = os.urandom(24)

class TestingConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Krutu%402001@localhost/task_manager1'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db')
    TESTING = True
    JWT_SECRET_KEY = 'your_testing_secret_key'
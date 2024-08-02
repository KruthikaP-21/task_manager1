from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, MetaData

db = SQLAlchemy()

# metadata = MetaData()
#
# user_table = Table('user', metadata,
#     # Column definitions
#     extend_existing=True
# )
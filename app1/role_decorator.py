from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from task_manager1.app1.models import User

def role_required(role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if current_user.role != role:
                return {'message': 'Access denied'}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


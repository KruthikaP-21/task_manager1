from flask import request
from flask_restful import Resource
from task_manager1.app1.models import Task, User
from task_manager1.app1.db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from task_manager1.app1.role_decorator import role_required


class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date,
            'created_at': task.created_at,
            'updated_at': task.updated_at,
            'user_id': task.user_id
        }

    @jwt_required()
    def put(self, task_id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
        data = request.get_json()
        task.title = data['title']
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.priority = data.get('priority', task.priority)
        task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if 'due_date' in data else task.due_date
        task.updated_at = datetime.utcnow()
        db.session.commit()
        return {'message': 'Task updated'}

    @jwt_required()
    def delete(self, task_id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted'}


class TaskList(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        filters = request.args.to_dict()
        page = int(filters.pop('page', 1))
        per_page = int(filters.pop('per_page', 10))

        query = Task.query.filter_by(user_id=current_user_id)

        if 'status' in filters:
            query = query.filter_by(status=filters['status'])
        if 'priority' in filters:
            query = query.filter_by(priority=filters['priority'])
        if 'due_date' in filters:
            due_date = datetime.strptime(filters['due_date'], '%Y-%m-%d')
            query = query.filter(Task.due_date <= due_date)
        if 'search' in filters:
            search = filters['search']
            query = query.filter((Task.title.ilike(f"%{search}%")) | (Task.description.ilike(f"%{search}%")))

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        tasks = pagination.items

        return {
            'tasks': [{
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': task.updated_at.strftime('%Y-%m-%d %H:%M:%S') if task.updated_at else None,
                'user_id': task.user_id
            } for task in tasks],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }

    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if 'due_date' in data else None
        if 'user_id' in data:
            user_id_here = data['user_id']
        else:
            user_id_here = current_user_id
        task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'Todo'),
            priority=data.get('priority', 1),
            due_date=due_date,
            user_id=user_id_here
        )
        db.session.add(task)
        db.session.commit()
        return {'message': 'Task created'}, 201


class TaskAssign(Resource):
    @role_required('Admin')
    @jwt_required()
    def post(self, task_id):
        data = request.get_json()
        task = Task.query.filter_by(id=task_id)
        user = User.query.get_or_404(data['user_id'])
        task.user_id = user.id
        db.session.commit()
        return {'message': 'Task assigned to user'}

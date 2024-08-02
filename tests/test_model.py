
import os

import pytest
from task_manager1.app1 import app
from task_manager1.app1.db import db
from datetime import datetime, timedelta
from task_manager1.app1.models import Task, User
from task_manager1.app1 import create_app

@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope='module')
def new_user():
    user = User(username='testuser')
    user.set_password('testpassword')
    return user


@pytest.fixture(scope='module')
def init_database(test_client, new_user):
    db.session.add(new_user)
    db.session.commit()
    yield db
    db.session.remove()

def get_access_token(test_client):
    response = test_client.post('/login', json={
        'username': 'admin',
        'password': 'newpassword'
    })
    return response.json['access_token']

def test_register_user(test_client):
    response = test_client.post('/register', json={
        'username': 'admin',
        'password': 'newpassword',
        'role': 'Admin'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'


def test_login_user(test_client, init_database):
    response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    print(response.json)
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_create_task(test_client, init_database):
    access_token = get_access_token(test_client)
    response = test_client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description',
        'status': 'Todo',
        'priority': 1,
        'due_date': (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    }, headers={'Authorization': f'Bearer {access_token}'})
    print(response.json)
    assert response.status_code == 201
    assert response.json['message'] == 'Task created'


def test_get_tasks(test_client, init_database):
    access_token = get_access_token(test_client)
    response = test_client.get('/tasks', headers={'Authorization': f'Bearer {access_token}'})
    print(response.json)
    assert response.status_code == 200
    assert len(response.json) > 0


def test_update_task(test_client, init_database):
    access_token = get_access_token(test_client)
    task = Task.query.filter_by(title='Test Task').first()
    response = test_client.put(f'/task/{task.id}', json={
        'title': 'Updated Task',
        'description': 'Updated Description',
        'status': 'In Progress',
        'priority': 2,
        'due_date': (datetime.utcnow() + timedelta(days=2)).strftime('%Y-%m-%d')
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Task updated'


def test_assign_task(test_client, init_database):
    access_token = get_access_token(test_client)
    new_user = User(username='anotheruser')
    new_user.set_password('anotherpassword')
    db.session.add(new_user)
    db.session.commit()
    task = Task.query.filter_by(title='Updated Task').first()
    response = test_client.post(f'/task/{task.id}/assign', json={
        'user_id': new_user.id
    }, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    assert response.json['message'] == 'Task assigned to user'

def test_delete_task(test_client, init_database):
    access_token = get_access_token(test_client)
    task = Task.query.filter_by(title='Updated Task').first()
    response = test_client.delete(f'/task/{task.id}', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted'

def test_filter_tasks(test_client, init_database):
    access_token = get_access_token(test_client)
    response = test_client.get('/tasks?status=Todo', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.json) > 0


def test_search_tasks(test_client, init_database):
    access_token = get_access_token(test_client)
    response = test_client.get('/tasks?search=Test', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.json) > 0

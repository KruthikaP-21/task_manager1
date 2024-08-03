
import pytest
from task_manager1.app1 import app
from task_manager1.app1.db import db
from datetime import datetime, timedelta
from task_manager1.app1.models import Task, User
from task_manager1.app1 import create_app

def test_new_user():
    # Unit Test
    user = User(username='testuser1')
    user.set_password('testpassword1')
    assert user.username == 'testuser1'
    assert user.check_password('testpassword1') == True

def test_new_task():
    due_date = datetime.utcnow() + timedelta(days=1)
    task = Task(
        title='Test Task',
        description='Test Description',
        status='Todo',
        priority=1,
        due_date=due_date
    )
    assert task.title == 'Test Task'
    assert task.description == 'Test Description'
    assert task.status == 'Todo'
    assert task.priority == 1
    assert task.due_date == due_date

def test_task_status_change():
    task = Task(
        title='Test Task',
        description='Test Description',
        status='Todo',
        priority=1,
        due_date=datetime.utcnow() + timedelta(days=1)
    )
    task.status = 'In Progress'
    assert task.status == 'In Progress'
    task.status = 'Done'
    assert task.status == 'Done'

def test_task_priority_change():
    task = Task(
        title='Test Task',
        description='Test Description',
        status='Todo',
        priority=1,
        due_date=datetime.utcnow() + timedelta(days=1)
    )
    task.priority = 2
    assert task.priority == 2

def test_task_due_date_change():
    new_due_date = datetime.utcnow() + timedelta(days=5)
    task = Task(
        title='Test Task',
        description='Test Description',
        status='Todo',
        priority=1,
        due_date=datetime.utcnow() + timedelta(days=1)
    )
    task.due_date = new_due_date
    assert task.due_date == new_due_date

def test_task_assignment():
    user = User(username='testuser')
    task = Task(
        title='Test Task',
        description='Test Description',
        status='Todo',
        priority=1,
        due_date=datetime.utcnow() + timedelta(days=1)
    )
    task.user_id = user.id
    assert task.user_id == user.id
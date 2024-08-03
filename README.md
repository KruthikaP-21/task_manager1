# Task Manager API

## Overview

The Task Manager API is a RESTful web service designed to manage tasks with features such as user registration and authentication, task creation, and assignment. This project is built using Flask and Docker and uses MySQL for data storage.

## Features

- **User Registration and Authentication**
- **CRUD Operations for Tasks**
- **Task Assignment to Users**
- **Task Filtering and Searching**

## Project Structure
## Installation
### Prerequisites
- Docker
- Docker Compose
### Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/KruthikaP-21/task_manager1.git
    cd task_manager1
    ```

2. **Build and run the Docker containers:**

    ```sh
    docker-compose build
    ```

    This command will build the container

    To use the flask app(for testing the api with postman), simply run
    ```sh
    docker-compose up web db
    ```

## Environment Variables

The application requires the following environment variables to be set:

- `FLASK_APP`: The entry point for the Flask application (set to `app1.app`).
- `FLASK_ENV`: The environment mode for Flask (set to `production` or `testing`).
- `SQLALCHEMY_DATABASE_URI`: The SQLAlchemy connection string for the MySQL database.
- `SECRET_KEY`: A secret key used by Flask for session management and other cryptographic operations.

## Usage

### Running the Flask Application

By default, the `web` service will start the Flask application. To access the application, visit:

```
http://localhost:5000
```

### Running Tests

To run tests, use the following command:

```sh
docker-compose run test
```

This command will execute the tests using `pytest`.

## API Endpoints

### User Registration

- **POST** `/register`
  
  Request body:
  
  ```json
  {
    "username": "newuser",
    "password": "newpassword"
  }
  ```

  Response:
  
  ```json
  {
    "message": "User created successfully"
  }
  ```

### User Login

- **POST** `/login`

  Request body:
  
  ```json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```

  Response:
  
  ```json
  {
    "access_token": "<jwt_token>"
  }
  ```

### Task Operations

- **GET** `/tasks` - Get a list of tasks.
- **POST** `/tasks` - Create a new task.
- **GET** `/task/<task_id>` - Get details of a specific task.
- **PUT** `/task/<task_id>` - Update a specific task.
- **DELETE** `/task/<task_id>` - Delete a specific task.
- **POST** `/task/<task_id>/assign` - Assign a task to a user. This is priviledged- only the user with the role as Admin can assign tasks to different users. Tasks created by user are by default assigned to the user himself 

### Task Filtering and Searching

- **GET** `/tasks?status=<status>&priority=<priority>&due_date=<due_date>` - Filter tasks based on status, priority, and due date.
- **GET** `/tasks/search?q=<query>` - Search tasks by title or description.

### Pagination of tasks
- To handle pagination in task lists, use the following query parameters:
- page: The page number to retrieve (default is 1).
- per_page: The number of tasks per page (default is 10).
  
- **GET** `/tasks?status=<status>&priority=<priority>&due_date=<due_date>` - Filter tasks based on status, priority, and due date.
- **GET** `/tasks/search?q=<query>` - Search tasks by title or description.  

## Docker

### Dockerfile

The `Dockerfile` sets up the Flask application environment. It uses Python 3.9 and installs the necessary dependencies listed in `requirements.txt`.

### Docker Compose

The `docker-compose.yml` file configures the services for the project:

- **db**: MySQL database service.
- **web**: Flask application service.
- **test**: Service for running tests.

For using local MySQL Database, change the SQLALCHEMY_DATABASE_URI: mysql+pymysql://root:..... and MYSQL_ROOT_PASSWORD to your own credentials in the docker-compose.yaml file
API Documentation can be found here: https://docs.google.com/document/d/1oze-GFqvaE6DWL7roB_14ifXalARRhm2iZ7m8Pk-aw4/edit?usp=sharing

If you don't want to use mysql, simply change the SQLALCHEMY_DATABASE_URI in app1/config.py to SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

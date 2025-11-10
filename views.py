from flask import Blueprint, render_template, redirect, url_for
from flask import request
from flask_login import login_required, current_user
from models import db, Task, User

# Create a blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def todo():
    return render_template('todo.html')


@main_blueprint.route('/api/v1/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return {
        "tasks": [task.to_dict() for task in tasks]
    }

@main_blueprint.route('/api/v1/tasks', methods=['POST'])
@login_required
def api_create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return {
        "task": new_task.to_dict()
    }, 201

@main_blueprint.route('/api/v1/toggle/<int:task_id>')
@login_required
def toggle(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return {}, 400
    
    task.toggle()
    db.session.commit()

    return {}, 200

@main_blueprint.route('/api/v1/edit/<int:task_id>', methods=["PUT"])
@login_required
def edit(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return {}, 400
    
    data = request.get_json()
    task.title = data['title']
    db.session.commit()

    return {}, 200


@main_blueprint.route('/api/v1/remove/<int:task_id>', methods=['DELETE'])
@login_required
def remove(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return {}, 400
    db.session.delete(task)
    db.session.commit()
    return {}, 200
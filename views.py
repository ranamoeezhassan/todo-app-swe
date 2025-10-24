from flask import Blueprint, render_template, redirect, url_for
from flask import request
from task import Task
from flask_login import login_required, current_user
from models import db, Task, User

# Create a blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        task = request.form['task-text']
        print(task)
        new_task = Task(title=task, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('todo.html', tasks=tasks)


@main_blueprint.route('/check/<int:task_id>')
@login_required
def check(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return redirect(url_for('main.todo'))
    
    task.toggle()
    db.session.commit()

    return redirect(url_for('main.todo'))


@main_blueprint.route('/remove/<int:task_id>')
@login_required
def remove(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return redirect(url_for('main.todo'))

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('main.todo'))
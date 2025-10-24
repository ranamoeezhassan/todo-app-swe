from flask import Blueprint, render_template, redirect, url_for
from flask import request
from task import Task

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

TASKS = []

@main_blueprint.route('/', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        task = request.form['task-text']
        new_task = Task(title=task)
        TASKS.append(new_task)

    return render_template('todo.html', tasks=TASKS)


@main_blueprint.route('/check/<int:task_id>')
def check(task_id):
    task = next((t for t in TASKS if t.id == task_id), None)

    if task is None:
        return redirect(url_for('main.todo'))
    
    task.toggle()

    return redirect(url_for('main.todo'))


@main_blueprint.route('/remove/<int:task_id>')
def remove(task_id):
    task = next((t for t in TASKS if t.id == task_id), None)

    if task is None:
        return redirect(url_for('main.todo'))

    TASKS.remove(task)

    return redirect(url_for('main.todo'))
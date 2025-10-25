from flask import Blueprint, render_template, redirect, url_for
from flask import request
from task import Task

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

TASKS = []

@main_blueprint.route('/', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        title = request.form.get('task-text')
        priority = request.form.get('priority', 'low')  # Default to 'low' if not specified
        if title:
            TASKS.append(Task(title, priority))

    return render_template('todo.html', tasks=TASKS)


@main_blueprint.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    for task in TASKS:
        if task.id == task_id:
            task.toggle()
            return redirect(url_for('main.todo'))
    return redirect(url_for('main.todo'))

@main_blueprint.route('/remove/<int:task_id>')
def remove(task_id):
    for task in TASKS:
        if task.id == task_id:
            TASKS.remove(task)
            return redirect(url_for('main.todo'))
    return redirect(url_for('main.todo'))
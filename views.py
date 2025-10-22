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
        if title:
            TASKS.append(Task(title))

    return render_template('todo.html', tasks=TASKS)


@main_blueprint.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    for task in TASKS:
        if task.id == task_id:
            task.toggle()
            return redirect(url_for('main.todo'))
    return redirect(url_for('main.todo'))
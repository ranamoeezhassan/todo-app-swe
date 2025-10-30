from flask import Blueprint, render_template, redirect, url_for
from flask import request, jsonify
from flask_login import login_required, current_user
from models import db, Task, User

# Create a blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        task = request.form['task-text']
        priority = request.form['priority']
        print(task)
        new_task = Task(title=task, user_id=current_user.id, priority=priority)
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

@main_blueprint.route('/edit/<int:task_id>', methods=['PUT', 'PATCH'])
@login_required
def edit(task_id):
    task = Task.query.get(task_id)

    if task is None or task.user_id != current_user.id:
        return jsonify({'error': 'Task not found'}), 404

    # Get JSON data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update task title if provided
    if 'title' in data:
        new_title = data['title'].strip()
        if not new_title:
            return jsonify({'error': 'Title cannot be empty'}), 400
        task.title = new_title
    
    # Update priority if provided
    if 'priority' in data:
        if data['priority'] in ['low', 'medium', 'high']:
            task.priority = data['priority']
        else:
            return jsonify({'error': 'Invalid priority'}), 400
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'priority': task.priority,
                'status': task.status
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task'}), 500
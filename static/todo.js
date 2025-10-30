// Task editing functionality

let editingTaskId = null;

function editTask(taskId) {
    // If already editing a task, cancel it first
    if (editingTaskId && editingTaskId !== taskId) {
        cancelEdit(editingTaskId);
    }

    const taskElement = document.querySelector(`li[data-id="${taskId}"]`);
    const titleLink = taskElement.querySelector('a[href^="/check/"]');
    const currentTitle = titleLink.textContent.trim();

    // Create input field for editing
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.value = currentTitle;
    inputField.className = 'edit-input';
    inputField.dataset.originalTitle = currentTitle;

    const saveBtn = document.createElement('button');
    saveBtn.textContent = '✓';
    saveBtn.className = 'save-btn';
    saveBtn.onclick = () => saveTask(taskId);

    const cancelBtn = document.createElement('button');
    cancelBtn.textContent = '✗';
    cancelBtn.className = 'cancel-btn';
    cancelBtn.onclick = () => cancelEdit(taskId);

    const editContainer = document.createElement('div');
    editContainer.className = 'edit-container';
    editContainer.appendChild(inputField);
    editContainer.appendChild(saveBtn);
    editContainer.appendChild(cancelBtn);

    titleLink.style.display = 'none';
    titleLink.parentNode.insertBefore(editContainer, titleLink);

    inputField.focus();
    inputField.select();

    inputField.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            saveTask(taskId);
        }
    });

    inputField.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            cancelEdit(taskId);
        }
    });

    editingTaskId = taskId;
}

async function saveTask(taskId) {
    const taskElement = document.querySelector(`li[data-id="${taskId}"]`);
    const inputField = taskElement.querySelector('.edit-input');
    const newTitle = inputField.value.trim();

    if (!newTitle) {
        alert('Task title cannot be empty!');
        inputField.focus();
        return;
    }

    try {
        const response = await fetch(`/edit/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: newTitle
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // Update the UI with the new title
            const titleLink = taskElement.querySelector('a[href^="/check/"]');
            titleLink.textContent = data.task.title;

            // Remove edit container and show title again
            finishEdit(taskId);

        } else {
            alert(data.error || 'Failed to update task');
        }
    } catch (error) {
        console.error('Error updating task:', error);
        alert('Failed to update task. Please try again.');
    }
}

function cancelEdit(taskId) {
    finishEdit(taskId);
}

function finishEdit(taskId) {
    const taskElement = document.querySelector(`li[data-id="${taskId}"]`);
    const editContainer = taskElement.querySelector('.edit-container');
    const titleLink = taskElement.querySelector('a[href^="/check/"]');

    if (editContainer) {
        editContainer.remove();
    }

    if (titleLink) {
        titleLink.style.display = '';
    }

    editingTaskId = null;
}


// Global keyboard shortcuts
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && editingTaskId) {
        cancelEdit(editingTaskId);
    }
});
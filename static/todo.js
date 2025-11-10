
// add item to todo list
function addTaskToList(task) {
  const taskList = document.getElementById('task-list');
  const li = document.createElement('li');
  li.innerHTML = `
    <a href="#" onclick="toggleTask(${task.id})">${task.title}</a>
    <a href="#" onclick="editTask(${task.id})">✏️</a>
    <a href="#" id="task-${task.id}" class="remove-btn" onclick="removeTask(${task.id})">🗑️</a>
  `;
  
  taskList.appendChild(li);
}

function editTask(taskId) {
  const li = document.getElementById(`task-${taskId}`).closest('li');
  const taskLink = li.querySelector('a');
  const currentTitle = taskLink.textContent;
  
  li.innerHTML = `
    <input type="text" value="${currentTitle}" onkeypress="if(event.key==='Enter') updateTask(${taskId}, this.value)">
    <button onclick="updateTask(${taskId}, this.previousElementSibling.value)">✓</button>
    <button onclick="loadTasks(); location.reload()">✗</button>
  `;
}

function updateTask(taskId, newTitle) {
  fetch(`/api/v1/edit/${taskId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: newTitle })
  })
  .then(response => response.json())
  .then(() => {
    location.reload(); // Refresh to show updated task
  });
}

// submit new task to API
const taskForm = document.getElementById('task-form');
taskForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const taskInput = document.getElementById('new-task');
  const taskTitle = taskInput.value.trim();

  if (taskTitle) {
    fetch('/api/v1/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title: taskTitle })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Task added:', data);
        taskInput.value = ''; // Clear the input
        addTaskToList(data.task); // Add the new task to the list
      });
  }
});

// Fetch and display tasks
function loadTasks() {
  // Clear existing tasks first
  document.getElementById('task-list').innerHTML = '';
  
  fetch('/api/v1/tasks')
    .then(response => response.json())
    .then(data => {
      data.tasks.forEach(task => {
        addTaskToList(task);
      });
    });
}

// remove task function
function removeTask(taskId) {
  console.log(`Removing task with ID: ${taskId}`);
  fetch(`/api/v1/remove/${taskId}`, { method: 'DELETE' })
    .then(response => {
      if (response.ok) {
        document.getElementById(`task-${taskId}`).closest('li').remove();
      }
    });
}

// toggle task function
function toggleTask(taskId) {
  console.log(`Toggling task with ID: ${taskId}`);
  fetch(`/api/v1/toggle/${taskId}`, { method: 'GET' })
    .then(response => {
      if (response.ok) {
        document.getElementById(`task-${taskId}`).closest('li').classList.toggle("completed");
      }
    });
}


// main function calls
loadTasks();
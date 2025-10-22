class Task():

    _task_id = 1

    def __init__(self, title):
        self.title = title
        self.id = Task._task_id
        Task._task_id += 1
        self.status = "not-completed"

    def toggle(self):
        if self.status == "not-completed":
            self.status = "completed"
        else:
            self.status = "not-completed"

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"


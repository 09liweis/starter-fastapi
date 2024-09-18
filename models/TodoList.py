class TodoList:

  def __init__(self, todos):
    self.todos = todos

  def getTodoCounts(self):
    todos = self.todos
    total_count = 0
    pending_count = 0
    done_count = 0
    for todo in todos:
      total_count += 1
      todo_status = todo['status']
      if todo_status == 'pending':
        pending_count += 1
      if todo_status == 'done':
        done_count += 1
    return {
        "name": "todo",
        "details": {
            "total": total_count,
            "pending": pending_count,
            "done": done_count,
        }
    }
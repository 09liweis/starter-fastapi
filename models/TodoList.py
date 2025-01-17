from models.Todo import Todo


class TodoList:

  def __init__(self, todos):
    self.todos = [Todo(todo) for todo in todos]

  def getTodoCounts(self):
    return {
        "name": "todo",
        "details": {
            "total": len(self.todos),
            "pending": len([todo for todo in self.todos if todo.is_pending()]),
            "done": len([todo for todo in self.todos if todo.is_done()])
        }
    }

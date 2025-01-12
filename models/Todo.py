class Todo:

  def __init__(self, todo):
    self.name = todo['name']
    self.status = todo['status']
  
  def get_name(self):
    return self.name

  def get_status(self):
    return self.status

  def is_done(self):
    return self.status == 'done'

  def is_pending(self):
    return self.status == 'pending'

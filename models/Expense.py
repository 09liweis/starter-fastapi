class Expense:

  def __init__(self, expense):
    self.price = expense['price']
    self.date = expense['date']
    self.category = expense['category']

  def getYear(self):
    return self.date[:4]

  def getMonth(self):
    return self.date[:7]

  def getPrice(self):
    return self.price

  def getCategory(self):
    return self.category

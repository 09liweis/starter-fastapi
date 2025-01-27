class Expense:

  def __init__(self, expense):
    self.price = expense['price']
    self.date = expense['date']
    self.category = expense['category']

  def get_year(self):
    return self.date[:4]

  def get_month(self):
    return self.date[:7]

  def get_price(self):
    return self.price

  def get_category(self):
    return self.category

  def is_income(self):
    return self.price > 0

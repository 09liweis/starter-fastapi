from models.Expense import Expense


class ExpenseList:

  def __init__(self, expenses):
    self.expenses = expenses

  def getExpenseCounts(self):
    result_details = {}
    for expense in self.expenses:
      ex = Expense(expense)
      yearDate = ex.get_year()
      yearMonthDate = ex.get_month()
      price = ex.get_price()
      category = ex.get_category()
      self._add_expense_to_details(result_details, yearDate, price, category)
      self._add_expense_to_details(result_details, yearMonthDate, price,
                                   category)
    return {"name": "expense", "details": result_details}

  def _add_expense_to_details(self, result_details, date, price, category):
    if date not in result_details:
      result_details[date] = {"total": price}
    else:
      result_details[date]["total"] += price
    if category in result_details[date]:
      result_details[date][category] += price
    else:
      result_details[date][category] = price

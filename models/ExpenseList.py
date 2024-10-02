class ExpenseList:

  def __init__(self, expenses):
    self.expenses = expenses

  def getExpenseCounts(self):
    expenses = self.expenses
    result_details = {}
    for expense in expenses:
      date = expense["date"]
      price = expense["price"]

      # year expense
      if (yearDate := date[:4]) not in result_details:
        result_details[yearDate] = {"total": price}
      else:
        result_details[yearDate]["total"] += price

      #year category expense
      if (category := expense["category"]) in result_details[yearDate]:
        result_details[yearDate][category] += price
      else:
        result_details[yearDate][category] = price

      #month expense
      if (yearMonthDate := date[:7]) not in result_details:
        result_details[yearMonthDate] = {"total": price}
      else:
        result_details[yearMonthDate]["total"] += price

      #month category expense
      if category in result_details[yearMonthDate]:
        result_details[yearMonthDate][category] += price
      else:
        result_details[yearMonthDate][category] = price
    return {"name": "expense", "details": result_details}

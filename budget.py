class Category:

  def __init__(self, categories):
      self.categories = categories
      self.ledger = []
      self._balance = 0.0

  def deposit(self, amount, description=''):
      self.ledger.append({"amount":amount, "description":description})
      self._balance += amount

  def withdraw(self, amount, description=''):
      if amount > self._balance:
          return False 
      self.ledger.append({"amount":-amount, "description":description})
      self._balance -= amount
      return True

  def get_balance(self):
      totals = []
      for led in self.ledger:
          totals.append(led['amount'])
      totals = sum(totals)
      return round(totals, 2)

  def transfer(self, amount, dest):
      if amount > self._balance:
          return False
      description = f'Transfer from {self.categories}'
      dest.ledger.append({"amount":amount, "description":description})
      dest._balance += amount

      description = f'Transfer to {dest.categories}'
      self.ledger.append({"amount":-amount, "description":description})
      self._balance -= amount
      return True

  def check_funds(self, amount):
      if amount > self._balance:
          return False
      return True

  def __str__(self) -> str:
      description = []
      am = []
      for i in self.ledger:
          description.append(i['description'])
          am.append(i['amount'])
      amount = [f'{float(j):.2f}' for j in am]
      total = self._balance

      n_mid = int((30 - len(self.categories)) / 2)

      result = ''
      result += '*'*n_mid+self.categories+'*'*n_mid+'\n'
      for x in range(len(amount)):
          result += f'{description[x][:23].ljust(23)}{amount[x].rjust(7)}\n'
      result += f'Total: {total:.2f}'
      return result

def create_spend_chart(lst_categories):
  lenc = len(lst_categories)
  lenstrip = lenc*3+1
  lenspace = 4

  lst_spent = []
  for categories in lst_categories:
      lst_amount = [x['amount'] for x in categories.ledger]
      spent = 0
      for amount in lst_amount:
          if amount > 0:
              continue
          spent += abs(amount)
      lst_spent.append(round(spent,0))
  total = sum(lst_spent)
  spent_percent = list(map(lambda amount: int((((amount/total)*10)//1)*10), lst_spent))

  chart = 'Percentage spent by category\n'
  for val in reversed(range(0, 101, 10)):
      chart += str(val).rjust(3)+'|'
      for percent in spent_percent:
          if percent >= val:
              chart += ' o '
          else:
              chart += '   '
      chart += ' \n'
  chart += ' '*lenspace + '-'*lenstrip
  category = []
  categories = [y.categories for y in lst_categories]
  longest = len(max(categories, key=len))
  new_categories = list(map(lambda _category: _category.ljust(longest), categories))
  for x in zip(*new_categories):
      category.append(' '*lenspace + ''.join(map(lambda s: s.center(3), x)) + ' ')
  category = '\n'.join(category)
  return '\n'.join([chart,category])

import re

class Category:
  def __init__(self,nam):
    self.name = nam
    self.ledger = []
    self.balance = 0

  def get_balance(self):
    return self.balance

  def check_funds(self, amount):
    return True if amount <= self.balance else False

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.balance += amount

  def withdraw(self, amount, description=""):
    if self.check_funds(amount) == True:
      self.ledger.append({"amount": -amount, "description": description})
      self.balance -= amount
      return True
    else:
      return False
  
  def transfer(self, amount, category):
    if self.check_funds(amount) == True:
      self.withdraw(amount, "Transfer to " + category.name)
      category.deposit(amount, "Transfer from " + self.name)
      return True
    else:
      return False
  
  def __str__(self):
    string = ""
    string += self.name.center(30,'*') + '\n'
    for transaction in self.ledger:
        string += transaction["description"][:23]
        string += str(format(float(transaction["amount"]), '.2f')).rjust(30 - len(transaction["description"][:23]))
        string += '\n'
    string += "Total: " + str(format(float(self.balance), '.2f'))
    return string

  # def print_ledger(self):
  #   print(self.name)
  #   print(self.ledger)

def longest_len_str(lst):
  longest = ""
  for str in lst:
    if len(str) > len(longest):
      longest = str
  return len(longest)

def create_spend_chart(categories):
  name_cat = []
  spending_all = []
  spending_by_cat = []
  perc_lst = []
  ## Parsing the name of the categories and all the spendings
  for category in categories:
    spending_all.append(re.findall(r'-\d*\.?\d+', str(category)))
    name_cat.append(re.findall('\*([A-Z][a-z]+)', str(category)[:30]))
  # name_cat.append(re.findall('[A-Z][a-z]+', str(categories[0-3])))
  ## Storing the double list "name_cat" into a single list "lst"
  lst = []
  i = 0
  while i < len(name_cat):
    lst.append(name_cat[i][0])
    i += 1
  ## Dividing the spendings by category and the total amount spent
  for list in spending_all:
    spending = 0
    for str_nb in list:
      spending += float(str_nb)
    spending_by_cat.append(spending)
  total_spending = sum(spending_by_cat)
  ## Getting the percentage spent by category stored in a list
  for spending in spending_by_cat:
    perc_lst.append((spending / total_spending) * 100)
  bar_chart = ""
  bar_chart += "Percentage spent by category\n"
  ## The chart
  perc = 100
  while perc != -10:
    bar_chart += str(perc).rjust(3) + "| "
    for perc_cat in perc_lst:
      if perc_cat >= perc:
        bar_chart += "o".ljust(3)
      else:
        bar_chart += '   '
    bar_chart += '\n'
    perc -= 10
  bar_chart += ' ' * 4 + '-' * (len(lst) * 3 + 1) + '\n'
  ## Writing the name of the categories vertically
  longest_cat = longest_len_str(lst)
  vertical_cat = ""
  for i in range(longest_cat):
    vertical_cat += "    "
    for name in lst :
      try :
        vertical_cat += name[i].center(3)
      except IndexError:
        vertical_cat += "   "
    vertical_cat += " "
    if i != longest_cat -1 :
      vertical_cat += "\n"
  bar_chart += vertical_cat
  return bar_chart
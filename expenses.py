expenses_data = []
rent_amount = 0

def add_expense(category, amount, person):
    expense = {
        'category': category,
        'amount': amount,
        'person': person,
    }
    expenses_data.append(expense)

def add_rent(amount):
    global rent_amount
    rent_amount = amount

def calculate_monthly_expenses():
    total = sum(e['amount'] for e in expenses_data if not (e['category'] in ['Gas', 'Cooking']))
    total += rent_amount
    return total
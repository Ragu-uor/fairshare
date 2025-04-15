from datetime import datetime
from models import get_user_id, sum_user_expense

def calculate_shares(users, expenses):
    # Calculate total days for rent sharing
    total_days = 0
    user_days = {}  # Dictionary to store each user's days
    for user in users:
        start_date = datetime.strptime(user['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(user['end_date'], '%Y-%m-%d')
        days = (end_date - start_date).days + 1  # Include the end date
        mnth = start_date.month
        total_days += days
        user_days[user['username']] = days  # Store the number of days for each user

    # Count users sharing grocery expenses
    grocery_sharing_users = [user for user in users if not user['exclude_grocery']]
    num_grocery_sharing_users = len(grocery_sharing_users)

    # Calculate shares
    shares = {}
    for user in users:
        days = user_days[user['username']]  # Get the number of days for the current user
        u_name = user['username']
        u_id = get_user_id(u_name)
        # Calculate rent share based on the user's stay period
        rent_share = (expenses['rent'] / total_days) * days

        # Calculate grocery share if not excluded
        grocery_share = 0
        if not user['exclude_grocery'] and num_grocery_sharing_users > 0:
            # Calculate grocery share based on the user's stay period
            total_grocery_days = sum(user_days[usr['username']] for usr in grocery_sharing_users)
            grocery_share = (expenses['grocery'] / total_grocery_days) * days

        # Calculate electricity and gas shares (assuming all share equally)
        electricity_share = (expenses['electricity'] / total_days) * days
        gas_share = (expenses['gas'] / total_days) * days

        # electricity_share = expenses['electricity'] / len(users)
        # gas_share = expenses['gas'] / len(users)
        user_already_spent = sum_user_expense(u_id, mnth)

        # Total share for the user
        total_share = rent_share + grocery_share + electricity_share + gas_share - float(user_already_spent[0])
        shares[user['username']] = {
            'Rent share': round(rent_share, 2),
            'Grocery share': round(grocery_share, 2),
            'Electricity share': round(electricity_share, 2),
            'Gas share': round(gas_share, 2),
            'Already spent': round(float(user_already_spent[0]), 2),
            'Total share': round(total_share, 2)
        }

    return shares

    

# # Example usage
# users = [
#     {'username': 'admin', 'start_date': '2025-04-01', 'end_date': '2025-04-30', 'exclude_grocery': False},
#     {'username': 'user1', 'start_date': '2025-04-01', 'end_date': '2025-04-10', 'exclude_grocery': False},
#     {'username': 'user2', 'start_date': '2025-04-01', 'end_date': '2025-04-30', 'exclude_grocery': True}
# ]

# expenses = {
#     'rent': 1200,
#     'grocery': 300,
#     'electricity': 100,
#     'gas': 50
# }

# shares = calculate_shares(users, expenses)
# print(shares)

# # Calculate total share to verify it sums to total rent
# total_rent_share = sum(share['rent_share'] for share in shares.values())
# print(f"Total Rent Share: {total_rent_share}")

# total_gas_share = sum(share['gas_share'] for share in shares.values())
# print(f"Total Gas Share: {total_gas_share}")

# total_electricity_share = sum(share['electricity_share'] for share in shares.values())
# print(f"Total Electricity Share: {total_electricity_share}")

# # Calculate total grocery share to verify it sums to total grocery
# total_grocery_share = sum(share['grocery_share'] for share in shares.values())
# print(f"Total Grocery Share: {total_grocery_share}")
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import bcrypt
from expenses import expenses_data, add_expense, calculate_monthly_expenses, add_rent
from tasks import tasks_data, assign_task
from users import users, check_user, is_admin
from models import get_user_id, add_expenses, add_task, get_all_users, expense_type_total, add_user, authenticate_user
from models import get_user_expenses, get_user_tasks, get_all_expenses, update_expense, remove_expense
from calculation import calculate_shares

app = Flask(__name__)
app.secret_key = "supersecretkey"  

#  Redirect to login page when visiting "/"
@app.route('/')
def index():
    return redirect(url_for('login'))  

# Login Route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         if check_user(username, password):
#             session['username'] = username
#             session['role'] = users[username]['role']  # Store user role
#             flash("Login successful!", "success")
#             return redirect(url_for('dashboard'))
#         else:
#             flash("Invalid login credentials!", "danger")

#     return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['user_mail']
        username = request.form['user_name']
        password = request.form['password']
        # Check if the checkbox for is_admin is checked
        is_admin = request.form.get('is_admin') == 'on'  # This will be True if checked, False if not

        # Call the add_user function to insert the user into the database
        if add_user(email, username, password, is_admin):
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash("Registration failed. Please try again.", "danger")
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = authenticate_user(email)

        if user:
            if (request.form['password'] == user['password']):
                print("Password is correct.")
                # Store user information in the session
                session['user_id'] = user['user_id']
                session['username'] = user['user_name']
                session['is_admin'] = user['is_admin']
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                print("Password is incorrect.")
        else:
            print("User  not found.")

        flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html')
#  Logout Route
# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash("Logged out successfully!", "info")
#     return redirect(url_for('login'))

#  Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    
    username = session['username']
    u_id = session['user_id']
    admin = session['is_admin']
    total_expenses = calculate_monthly_expenses()
    
    return render_template(
        'dashboard.html',
        username=username,
        expenses = get_user_expenses(u_id),
        tasks=get_user_tasks(u_id),
        total_expenses=total_expenses,
        admin=admin
    )

#  Add Expense Route
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense_route():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    admin = session.get('is_admin', False)

    users = None if not admin else get_all_users()

    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])

        if admin:
            person = request.form.get('person')  
            u_id = get_user_id(person) if person and person != '-- Unassigned --' else None
        else:
            person = username
            u_id = session['user_id']

        status = add_expenses(u_id, category, amount)

        if status:
            flash("Expense added successfully!", "success")
        else:
            flash("Error adding expense", "error")
        return redirect(url_for('dashboard'))

    return render_template('add_expense.html', users=users, admin=admin)


#  Add Rent Route (Admin Only)
@app.route('/add_rent', methods=['GET', 'POST'])
def add_rent_route():
    if 'username' not in session or not is_admin(session['username']):
        flash("Access denied!", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        amount = float(request.form['amount'])
        add_rent(amount)
        flash("Rent added successfully!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('add_rent.html')

# Assign Task Route (Admin Only)
@app.route('/assign_task', methods=['GET', 'POST'])
def assign_task_route():
    # if 'username' not in session or not is_admin(session['username']):
    #     flash("Access denied!", "danger")
    #     return redirect(url_for('dashboard'))
    users = get_all_users()
    if request.method == 'POST':
        task = request.form['task']
        assigned_to = request.form['assigned_to']
        due_date = request.form['due_date']
        u_id = get_user_id(assigned_to)
        # assign_task(task, assigned_to, due_date)
        add_task(u_id, task, due_date)
        flash(f"Task '{task}' assigned to {assigned_to} with due date {due_date}.", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('assign_task.html', users=users)

@app.route('/view_expense')
def view_expense_route():
    expenses = get_all_expenses()
    return render_template('view_expense.html', expenses=expenses)

@app.route('/edit_expense', methods=['POST'])
def edit_expense():
    # logic to update the expenses
    expense_id = request.form['expense_id']
    user_id = request.form['user_id']
    amount = request.form['expense_amount']
    date = request.form['expense_date']
    expense_type = request.form['expense_type']
    update_expense(user_id, amount, date, expense_type, expense_id)

    return redirect(url_for('view_expense_route'))

@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    expense_id = request.form['expense_id']  
    remove_expense(expense_id)  
    return redirect(url_for('view_expense_route'))



@app.route('/generate_share', methods=['GET', 'POST'])
def generate_share():
    # Retrieve the list of users
    users = get_all_users()  # A function that fetches all users
    # print(users)  # Debugging line to check the structure of users

    if request.method == 'POST':
        # Extract form data from the request
        form_data = []
        for user_id, user in enumerate(users):  # Use enumerate to get index
            user_data = {
                'username': request.form.get(f"user_name_{user_id}"),  # Use user_id as index
                'start_date': request.form.get(f"start_date_{user_id}"),
                'end_date': request.form.get(f"end_date_{user_id}"),
                'exclude_grocery': f"exclude_grocery_{user_id}" in request.form  # Checkbox check
            }
            form_data.append(user_data)
        # You can then process the form data (e.g., save it to the database)
        # print(form_data)  # Debugging line to check the form data
        dte = datetime.strptime(form_data[0]['start_date'], '%Y-%m-%d')
        mnth = dte.month        
        expenses = {
            'rent': expense_type_total('Rent', mnth),
            'grocery': expense_type_total('Grocery', mnth),
            'electricity': expense_type_total('Electricity', mnth),
            'gas': expense_type_total('Gas', mnth)
        }
        shares = calculate_shares(form_data, expenses)
        # Store shares in session
        session['shares'] = shares

        return redirect(url_for('show_shares'))  # Redirect to the new route
    return render_template('generate_share.html', users=users)

@app.route('/show_shares')
def show_shares():
    shares = session.get('shares', {})
    return render_template('show_shares.html', shares=shares)


if __name__ == '__main__':
    app.run(debug=True)

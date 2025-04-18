from db import get_db_connection

def get_all_users():
    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT user_id, user_name FROM user_info')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    # print(users)
    # for user in users:
    #     print(user['user_name'])
    return(users)

def get_user_id(user_name):
    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT user_id FROM user_info WHERE user_name = %s', (user_name,))
    user_id = cursor.fetchone()  # Assuming user_name is unique and will return a single row
    cursor.close()
    connection.close()
    # print(user_id['user_id']) 
    return(user_id['user_id']) 

def add_user(email, username, password, is_admin):
    connection = get_db_connection()
    if connection is None:
        return False  # Return False if connection fails

    cursor = connection.cursor()
    try:
        # Define the query to insert the user data
        query = """
        INSERT INTO user_info (user_mail, password, user_name, is_admin) 
        VALUES (%s, %s, %s, %s);
        """

        # Execute the query with parameters
        cursor.execute(query, (email, password, username, is_admin))
        
        # Commit the transaction to save changes
        connection.commit()  # Only call commit if execution was successful
        return True  # Return True if insertion was successful

    except Exception as e:
        print(f"Error: {e}")
        # If there was an error, rollback the transaction to revert changes
        try:
            connection.rollback()  # Rollback the transaction in case of error
        except Exception as rollback_error:
            print(f"Rollback failed: {rollback_error}")
        return False  # Return False if there was an error

    finally:
        # Close the cursor and connection in the finally block to ensure they are always closed
        cursor.close()
        connection.close()

def authenticate_user(email):
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True) 
    try:
        query = "SELECT user_id, password, user_name, is_admin FROM user_info WHERE user_mail = %s;"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        return user  # Already a dictionary now, no need to map manually

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()
   

def add_expenses(user_id, category, amount):
    connection = get_db_connection()
    if connection is None:
        return False  # Return False if connection fails

    cursor = connection.cursor()
    try:
        # Define the query to insert the expense data
        query = """
        INSERT INTO expenses (user_id, expense_amount, expense_date, expense_type)
        VALUES (%s, %s, CURDATE(), %s);
        """

        # Execute the query with parameters
        cursor.execute(query, (user_id, amount, category))
        
        # Commit the transaction to save changes
        connection.commit()  # Only call commit if execution was successful
        return True  # Return True if insertion was successful

    except Exception as e:
        print(f"Error: {e}")
        # If there was an error, rollback the transaction to revert changes
        try:
            connection.rollback()  # Rollback the transaction in case of error
        except Exception as rollback_error:
            print(f"Rollback failed: {rollback_error}")
        return False  # Return False if there was an error

    finally:
        # Close the cursor and connection in the finally block to ensure they are always closed
        cursor.close()
        connection.close()

def add_task(user_id, task_summary, task_due_date):
    connection = get_db_connection()
    if connection is None:
        return False  # Return False if connection fails

    cursor = connection.cursor()
    try:
        # Define the query to insert the task data
        query = """
        INSERT INTO task_info (user_id, task_summary, task_due_date)
        VALUES (%s, %s, %s);
        """

        # Execute the query with parameters
        cursor.execute(query, (user_id, task_summary, task_due_date))
        
        # Commit the transaction to save changes
        connection.commit()  # Only call commit if execution was successful
        return True  # Return True if insertion was successful

    except Exception as e:
        print(f"Error: {e}")
        # If there was an error, rollback the transaction to revert changes
        try:
            connection.rollback()  # Rollback the transaction in case of error
        except Exception as rollback_error:
            print(f"Rollback failed: {rollback_error}")
        return False  # Return False if there was an error

    finally:
        # Close the cursor and connection in the finally block to ensure they are always closed
        cursor.close()
        connection.close()

def expense_type_total(type, mnth):
    # Establish a database connection
    connection =  get_db_connection()

    if connection is None:
        return False  # Return False if connection fails

    cursor = connection.cursor()

    try:        
        # Prepare the SQL query
        query = """
        SELECT SUM(expense_amount) AS total_expense
        FROM expenses
        WHERE MONTH(expense_date) = %s AND expense_type = %s;
        """
        
        # Execute the query with parameters
        cursor.execute(query, (mnth, type))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Return the total expense, or 0 if there are no results
        return result[0] if result[0] is not None else 0

    except Exception as err:  # Catching general exceptions
        print(f"Error: {err}")
        return None
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

def get_user_expenses(user_id):
    if user_id is None:
        return []

    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    query = '''
        SELECT expense_amount, expense_type FROM expenses
        WHERE user_id = %s
        ORDER BY expense_date DESC
    '''
    cursor.execute(query, (user_id,))
    expenses = cursor.fetchall()
    cursor.close()
    connection.close()

    return expenses

def get_user_tasks(user_id):
    if user_id is None:
        return []

    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    query = '''
        SELECT task_summary, task_due_date FROM `task_info`
        where user_id = %s
        order by task_due_date;
    '''
    cursor.execute(query, (user_id,))
    expenses = cursor.fetchall()
    cursor.close()
    connection.close()

    return expenses

def sum_user_expense(user_id, mnth):
    if user_id is None or mnth is None:
        return 0  # Return 0 if either user_id or month is missing

    connection = get_db_connection()
    if connection is None:
        return 0

    cursor = connection.cursor()
    query = '''
        SELECT 
            SUM(expense_amount) AS total_expense
        FROM 
            expenses
        WHERE 
            user_id = %s AND MONTH(expense_date) = %s
    '''
    cursor.execute(query, (user_id, mnth))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result

def get_all_expenses():
    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM `expenses`;'
    cursor.execute(query)
    expenses = cursor.fetchall()
    cursor.close()
    connection.close()
    return expenses

def update_expense(user_id, amount, date, expense_type, expense_id):
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed", 500

    cursor = connection.cursor()
    update_query = """
        UPDATE expenses
        SET user_id = %s,
            expense_amount = %s,
            expense_date = %s,
            expense_type = %s
        WHERE expense_id = %s
    """
    cursor.execute(update_query, (user_id, amount, date, expense_type, expense_id))
    connection.commit()
    cursor.close()
    connection.close()
    return True

def remove_expense(expense_id):
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed", 500

    cursor = connection.cursor()
    delete_query = "DELETE FROM expenses WHERE expense_id = %s"
    cursor.execute(delete_query, (expense_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return True





# u_e = get_all_expenses()
# print(u_e)






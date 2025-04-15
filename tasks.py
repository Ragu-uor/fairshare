tasks_data = []

def assign_task(task, assigned_to, due_date):
    task_entry = {
        'task': task,
        'assigned_to': assigned_to,
        'due_date': due_date
    }
    tasks_data.append(task_entry)

import json
import csv
from datetime import datetime

class Task:
    def __init__(self, title, description='', priority='Низкий', due_date=None):
        self.id = None
        self.title = title
        self.description = description
        self.done = False
        self.priority = priority
        self.due_date = due_date

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                return [self.dict_to_task(task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def dict_to_task(self, task_dict):
        task = Task(task_dict['title'], task_dict.get('description', ''), task_dict.get('priority', 'Низкий'), task_dict.get('due_date', None))
        task.id = task_dict['id']
        task.done = task_dict.get('done', False)
        return task

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([self.task_to_dict(task) for task in self.tasks], file)

    def task_to_dict(self, task):
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'done': task.done,
            'priority': task.priority,
            'due_date': task.due_date
        }

    def get_next_id(self):
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, title, description='', priority='Низкий', due_date=None):
        new_task = Task(title, description, priority, due_date)
        new_task.id = self.get_next_id()
        self.tasks.append(new_task)
        self.save_tasks()

    def view_tasks(self):
        return self.tasks

    def mark_task_done(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.done = True
                self.save_tasks()
                return True
        return False

    def edit_task(self, task_id, title=None, description=None, priority=None, due_date=None):
        for task in self.tasks:
            if task.id == task_id:
                if title:
                    task.title = title
                if description is not None:
                    task.description = description
                if priority:
                    task.priority = priority
                if due_date:
                    task.due_date = due_date
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    def export_to_csv(self, csv_filename):
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'title', 'description', 'done', 'priority', 'due_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for task in self.tasks:
                writer.writerow(self.task_to_dict(task))

    def import_from_csv(self, csv_filename):
        with open(csv_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.add_task(row['title'], row['description'], row['priority'], row['due_date'])

    def filter_tasks(self, status=None, priority=None, due_date=None):
        filtered_tasks = self.tasks
        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.done == status]
        if priority is not None:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]
        if due_date is not None:
            filtered_tasks = [task for task in filtered_tasks if task.due_date == due_date]
        return filtered_tasks

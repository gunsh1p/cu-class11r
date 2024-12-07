import json
import csv
from datetime import datetime
from collections import defaultdict
import texts

class FinanceRecord:
    def __init__(self, amount, category, date, description=''):
        self.id = None
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
    

class FinanceManager:
    def __init__(self, filename='finance.json'):
        self.filename = filename
        self.records = self.load_records()

    def load_records(self):
        try:
            with open(self.filename, 'r') as file:
                records_data = json.load(file)
                return [self.dict_to_record(record) for record in records_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def dict_to_record(self, record_dict):
        record = FinanceRecord(record_dict['amount'], record_dict['category'], record_dict['date'], record_dict.get('description', ''))
        record.id = record_dict['id']
        return record

    def save_records(self):
        with open(self.filename, 'w') as file:
            json.dump([self.record_to_dict(record) for record in self.records], file)

    def record_to_dict(self, record):
        return {
            'id': record.id,
            'amount': record.amount,
            'category': record.category,
            'date': record.date,
            'description': record.description
        }

    def get_next_id(self):
        if not self.records:
            return 1
        return max(record.id for record in self.records) + 1

    def add_record(self, amount, category, date, description=''):
        new_record = FinanceRecord(amount, category, date, description)
        new_record.id = self.get_next_id()
        self.records.append(new_record)
        self.save_records()

    def view_records(self):
        return [self.record_to_dict(record) for record in self.records]

    def filter_records(self, category=None, start_date=None, end_date=None):
        filtered = self.records
        if category:
            filtered = [record for record in filtered if record.category.lower() == category.lower()]
        if start_date:
            filtered = [record for record in filtered if datetime.strptime(record.date, "%d-%m-%Y") >= datetime.strptime(start_date, "%d-%m-%Y")]
        if end_date:
            filtered = [record for record in filtered if datetime.strptime(record.date, "%d-%m-%Y") <= datetime.strptime(end_date, "%d-%m-%Y")]
        return [self.record_to_dict(record) for record in filtered]

    def generate_report(self, start_date, end_date):
        filtered_records = self.filter_records(start_date=start_date, end_date=end_date)
        total_income = sum(record.amount for record in filtered_records if record.amount > 0)
        total_expense = sum(record.amount for record in filtered_records if record.amount < 0)
        
        report_filename = f'report_{start_date.strftime("%d-%m-%Y")}_{end_date.strftime("%d-%m-%Y")}.csv'

        with open(report_filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'amount', 'category', 'date', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for record in filtered_records:
                writer.writerow(self.record_to_dict(record))

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': total_income + total_expense,
            'records': filtered_records
        }

    def export_to_csv(self, csv_filename='finance.csv'):
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'amount', 'category', 'date', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for record in self.records:
                writer.writerow(self.record_to_dict(record))

    def import_from_csv(self, csv_filename='finance.csv'):
        with open(csv_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = FinanceRecord(float(row['amount']), row['category'], row['date'], row.get('description', ''))
                record.id = int(row['id'])
                self.records.append(record)
            self.save_records()

    def calculate_balance(self):
        total_income = sum(record.amount for record in self.records if record.amount > 0)
        total_expense = sum(record.amount for record in self.records if record.amount < 0)
        return total_income + total_expense

    def group_by_category(self):
        grouped = defaultdict(float)
        for record in self.records:
            grouped[record.category] += record.amount
        return dict(grouped)

def manage_finances(finance_manager: FinanceManager) -> None:
    print(texts.FINANCES)
    action = input("Выберите действие: ")
    if action == '1':
        amount = float(input("Введите сумму: "))
        category = input("Введите категорию: ")
        date = input("Введите дату (DD-MM-YYYY): ")
        description = input("Введите описание (необязательно): ")
        finance_manager.add_record(amount, category, date, description)
    elif action == '2':
        filtered = input("Добавить фильтры [Y/n]: ")
        if filtered.lower() == "y":
            category = input("Введите категорию: ")
            start_date = input("Введите начальную дату (DD-MM-YYYY): ")
            end_date = input("Введите конечную дату (DD-MM-YYYY): ")
            records = finance_manager.filter_records(category, start_date, end_date)
        else:
            records = finance_manager.view_records()
        print(records)
    elif action == '3':
        start_date = input("Введите начальную дату (DD-MM-YYYY): ")
        end_date = input("Введите конечную дату (DD-MM-YYYY): ")
        finance_manager.generate_report(start_date, end_date)
    elif action == '4':
        filename = input("Введите имя файла: ")
        finance_manager.export_to_csv(filename)
    elif action == '5':
        filename = input("Введите имя файла: ")
        finance_manager.import_from_csv(filename)

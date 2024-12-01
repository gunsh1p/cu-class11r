from notes import Note, NotesManager
from tasks import Task, TaskManager
from contacts import Contact, ContactsManager
from finances import FinanceRecord, FinanceManager
from calc import Calculator
import texts

def manage_notes(notes_manager: NotesManager) -> None:
    print(texts.NOTES)
    action = input("Выберите действие: ")
    if action == "1":
        title = input("Введите название: ")
        content = input("Введите содержимое заметки: ")
        notes_manager.create_note(title, content)
    elif action == "2":
        print(notes_manager.view_notes())
    elif action == "3":
        note_id = int(input("Введите id заметки: "))
        print(notes_manager.view_note_details(note_id))
    elif action == "4":
        note_id = int(input("Введите id заметки: "))
        title = input("Введите название: ")
        content = input("Введите содержимое заметки: ")
        notes_manager.edit_note(note_id, title, content)
    elif action == "5":
        note_id = int(input("Введите id заметки: "))
        notes_manager.delete_note(note_id)
    elif action == "6":
        filename = input("Введите имя файла: ")
        notes_manager.export_to_csv(filename)
    elif action == "7":
        filename = input("Введите имя файла: ")
        notes_manager.import_from_csv(filename)

def manage_tasks(task_manager: TaskManager) -> None:
    print(texts.TASKS)
    action = input("Выберите действие: ")
    if action == "1":
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        priority = input("Введите приоритет (Высокий, Средний, Низкий): ")
        due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
        task_manager.add_task(title, description, priority, due_date)
    elif action == "2":
        filtered = input("Добавить фильтры [Y/n]: ")
        if filtered.lower() == "y":
            status_input = input("Фильтровать по статусу (выполнена/не выполнена, оставьте пустым для пропуска): ")
            priority_input = input("Фильтровать по приоритету (Высокий, Средний, Низкий, оставьте пустым для пропуска): ")
            due_date_input = input("Фильтровать по сроку выполнения (ДД-ММ-ГГГГ, оставьте пустым для пропуска): ")
            status = None
            if status_input.lower() == 'выполнена':
                status = True
            elif status_input.lower() == 'не выполнена':
                status = False
            tasks = task_manager.filter_tasks(status, priority_input or None, due_date_input or None)
        else:
            tasks = task_manager.view_tasks()
        for task in tasks:
            print(f"{task.id}: {task.title} - {'Выполнена' if task.done else 'Не выполнена'}, Приоритет: {task.priority}, Срок: {task.due_date}")
    elif action == "3":
        task_id = int(input("Введите id задачи: "))
        task_manager.mark_task_done(task_id)
    elif action == "4":
        task_id = int(input("Введите id задачи: "))
        title = input("Введите новое название задачи (оставьте пустым для пропуска): ")
        description = input("Введите новое описание задачи (оставьте пустым для пропуска): ")
        priority = input("Введите новый приоритет (оставьте пустым для пропуска): ")
        due_date = input("Введите новый срок выполнения (оставьте пустым для пропуска): ")
        task_manager.edit_task(task_id, title or None, description or None, priority or None, due_date or None)
    elif action == "5":
        task_id = int(input("Введите id задачи: "))
        task_manager.delete_task(task_id)
    elif action == "6":
        filename = input("Введите имя файла: ")
        task_manager.export_to_csv(filename)
    elif action == "7":
        filename = input("Введите имя файла: ")
        task_manager.import_from_csv(filename)

def manage_contacts(contacts_manager: ContactsManager) -> None:
    print(texts.CONTACTS)
    action = input("Выберите действие: ")
    if action == '1':
        name = input("Введите имя контакта: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите email: ")
        contacts_manager.add_contact(name, phone, email)
    elif action == '2':
        search_term = input("Введите имя или номер для поиска: ")
        results = contacts_manager.search_contact(search_term)
        if results:
            print("Найденные контакты:")
            for contact in results:
                print(f"Имя: {contact.name}, Телефон: {contact.phone}")
        else:
            print("Контакты не найдены.")
    elif action == '3':
        contact_id = int(input("Введите id контакта: "))
        name = input("Введите имя контакта: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите email: ")
        contacts_manager.edit_contact(contact_id, name, phone, email)
    elif action == '4':
        contact_id = int(input("Введите id контакта: "))
        contacts_manager.delete_contact(contact_id)
    elif action == '5':
        filename = input("Введите имя файла: ")
        contacts_manager.export_to_csv(filename)
    elif action == '6':
        filename = input("Введите имя файла: ")
        contacts_manager.import_from_csv(filename)

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

def calculate(calculator: Calculator) -> None:
    expression = input("Введите выражение (например, \"2 + 2\"): ")
    result = calculator.calculate(expression)
    if result is not None:
        print(result)

def main():
    notes_manager = NotesManager()
    task_manager = TaskManager()
    contacts_manager = ContactsManager()
    finance_manager = FinanceManager()
    calculator = Calculator()

    print("Добро пожаловать в Персональный помощник!")

    while True:
        print(texts.GREETINGS)
        action = input("Выберите действие: ")
        if action == "1":
            manage_notes(notes_manager)
        elif action ==  "2":
            manage_tasks(task_manager)
        elif action == "3":
            manage_contacts(contacts_manager)
        elif action == "4":
            manage_finances(finance_manager)
        elif action == "5":
            calculate(calculator)
        else:
            break

if __name__ == "__main__":
    main()

from managers.notes import NotesManager, manage_notes
from managers.tasks import TaskManager, manage_tasks
from managers.contacts import ContactsManager, manage_contacts
from managers.finances import FinanceManager, manage_finances
from managers.calc import Calculator, calculate
import texts

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

import json
import csv

class Contact:
    def __init__(self, name, phone=None, email=None):
        self.id = None
        self.name = name
        self.phone = phone
        self.email = email

class ContactsManager:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, 'r') as file:
                contacts_data = json.load(file)
                return [self.dict_to_contact(contact) for contact in contacts_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def dict_to_contact(self, contact_dict):
        contact = Contact(contact_dict['name'], contact_dict.get('phone'), contact_dict.get('email'))
        contact.id = contact_dict['id']
        return contact

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump([self.contact_to_dict(contact) for contact in self.contacts], file)

    def contact_to_dict(self, contact):
        return {
            'id': contact.id,
            'name': contact.name,
            'phone': contact.phone,
            'email': contact.email
        }

    def get_next_id(self):
        if not self.contacts:
            return 1
        return max(contact.id for contact in self.contacts) + 1

    def add_contact(self, name, phone=None, email=None):
        new_contact = Contact(name, phone, email)
        new_contact.id = self.get_next_id()  # Получаем следующий ID
        self.contacts.append(new_contact)
        self.save_contacts()

    def search_contact(self, query):
        return [contact for contact in self.contacts if query.lower() in contact.name.lower() or (contact.phone and query in contact.phone)]

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            if name:
                contact.name = name
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            self.save_contacts()

    def delete_contact(self, contact_id):
        self.contacts = [contact for contact in self.contacts if contact.id != contact_id]
        self.save_contacts()

    def get_contact_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None

    def export_to_csv(self, csv_filename='contacts.csv'):
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'name', 'phone', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for contact in self.contacts:
                writer.writerow(self.contact_to_dict(contact))

    def import_from_csv(self, csv_filename='contacts.csv'):
        with open(csv_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                contact = Contact(row['name'], row.get('phone'), row.get('email'))
                contact.id = int(row['id'])
                self.contacts.append(contact)
            self.save_contacts()


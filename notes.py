import json
import csv
from datetime import datetime

class Note:
    def __init__(self, title, content=''):
        self.id = None
        self.title = title
        self.content = content
        self.timestamp = self.get_current_timestamp()

    @staticmethod
    def get_current_timestamp():
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

class NotesManager:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, 'r') as file:
                notes_data = json.load(file)
                return [self.dict_to_note(note) for note in notes_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def dict_to_note(self, note_dict):
        note = Note(note_dict['title'], note_dict['content'])
        note.id = note_dict['id']
        note.timestamp = note_dict['timestamp']
        return note

    def save_notes(self):
        with open(self.filename, 'w') as file:
            json.dump([self.note_to_dict(note) for note in self.notes], file)

    def note_to_dict(self, note):
        return {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'timestamp': note.timestamp
        }

    def get_next_id(self):
        if not self.notes:
            return 1
        return max(note.id for note in self.notes) + 1

    def create_note(self, title, content=''):
        new_note = Note(title, content)
        new_note.id = self.get_next_id()
        self.notes.append(new_note)
        self.save_notes()

    def view_notes(self):
        return [(note.id, note.title, note.timestamp) for note in self.notes]

    def view_note_details(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return self.note_to_dict(note)
        return None

    def edit_note(self, note_id, title=None, content=None):
        note = self.view_note_details(note_id)
        if note:
            if title:
                note.title = title
            if content:
                note.content = content
            note.timestamp = Note.get_current_timestamp()
            self.save_notes()

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()

    def export_to_csv(self, csv_filename='notes.csv'):
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'title', 'content', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for note in self.notes:
                writer.writerow(self.note_to_dict(note))

    def import_from_csv(self, csv_filename='notes.csv'):
        with open(csv_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                note = Note(row['title'], row['content'])
                note.id = int(row['id'])
                note.timestamp = row['timestamp']
                self.notes.append(note)
            self.save_notes()


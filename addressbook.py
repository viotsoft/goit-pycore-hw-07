from datetime import datetime
from fields import Name, Phone, Birthday
from decorators import input_error 

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return
        raise ValueError(f"Phone number {old_phone} not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = self.birthday.value.replace(year=today.year).date()
            if next_birthday < today:
                next_birthday = self.birthday.value.replace(year=today.year + 1).date()
            return (next_birthday - today).days
        return None

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name.value == name:
                return record
        return None

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []
        for record in self.records:
            days = record.days_to_birthday()
            if days is not None and 0 < days <= 7:
                upcoming_birthdays.append(record.name.value)
        return upcoming_birthdays

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for {name} updated."
    return f"Contact {name} not found."

@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        phones = ', '.join(phone.value for phone in record.phones)
        return f"{name}'s phone numbers: {phones}"
    return f"Contact {name} not found."

def show_all_contacts(book):
    result = []
    for record in book.records:
        phones = ', '.join(phone.value for phone in record.phones)
        result.append(f"{record.name.value}: {phones}")
    return "\n".join(result) if result else "No contacts in the book."

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)

    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)

    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."
    elif record:
        return f"{name} does not have a birthday set."
    else:
        return f"Contact {name} not found."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return f"Contacts with birthdays in the next week: {', '.join(upcoming_birthdays)}."
    else:
        return "No upcoming birthdays in the next week."

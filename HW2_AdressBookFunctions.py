from datetime import datetime, timedelta


class Birthday:
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")

class Name:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Phone:
    def __init__(self, number):
        if not self.validate_phone(number):
            raise ValueError("Invalid phone number format.")
        self.number = number

    def validate_phone(self, number):
        return len(number) > 0

    def __str__(self):
        return self.number

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def __str__(self):
        phones = ', '.join(str(phone) for phone in self.phones)
        birthday = str(self.birthday) if self.birthday else "No birthday"
        return f"Name: {self.name}, Phones: {phones}, Birthday: {birthday}"

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name.name == name:
                return record
        return None

    def get_upcoming_birthdays(self):
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.records:
            if record.birthday:
                birthday = record.birthday.date
                birthday_this_year = birthday.replace(year=today.year)
                if today <= birthday_this_year < today + timedelta(days=7):
                    upcoming_birthdays.append(record)
        return upcoming_birthdays


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return str(e)
    return wrapper


@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    record.add_birthday(date)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    return str(record.birthday) if record.birthday else "No birthday."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No birthdays upcoming."
    return '\n'.join(str(record) for record in upcoming_birthdays)

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
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    for phone in record.phones:
        if phone.number == old_phone:
            phone.number = new_phone
            return "Phone number updated."
    raise ValueError("Old phone number not found.")

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    return ', '.join(str(phone) for phone in record.phones) if record.phones else "No phone numbers."

@input_error
def show_all_contacts(args, book):
    if not book.records:
        return "No contacts in the address book."
    return '\n'.join(str(record) for record in book.records)



def parse_input(user_input):
    return user_input.split()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

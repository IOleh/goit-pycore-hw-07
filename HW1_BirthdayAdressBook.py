from datetime import datetime, timedelta

class Birthday:
    def __init__(self, value):
        try:
            # Спробуємо перетворити рядок на об'єкт datetime
            self.date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        # Повертаємо дату у форматі DD.MM.YYYY
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
        # Простий приклад перевірки формату номера телефону
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

    def get_upcoming_birthdays(self):
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.records:
            if record.birthday:
                # Визначаємо, чи день народження припадає на наступний тиждень
                birthday = record.birthday.date
                birthday_this_year = birthday.replace(year=today.year)
                if today <= birthday_this_year < today + timedelta(days=7):
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

# Тестування функціональності
if __name__ == "__main__":
    # Створюємо об'єкт AddressBook
    book = AddressBook()

    # Додаємо записи
    record1 = Record("Alice")
    record1.add_phone("123456789")
    record1.add_birthday("05.08.2024")
    book.add_record(record1)

    record2 = Record("Bob")
    record2.add_phone("987654321")
    record2.add_birthday("10.08.2024")
    book.add_record(record2)

    # Отримуємо список контактів з днями народження наступного тижня
    upcoming_birthdays = book.get_upcoming_birthdays()
    for record in upcoming_birthdays:
        print(record)

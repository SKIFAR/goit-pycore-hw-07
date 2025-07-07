from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self):
        date_today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            contact_birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = contact_birthday.replace(year=date_today.year)

            if birthday_this_year < date_today:
                birthday_this_year = birthday_this_year.replace(year=date_today.year + 1)

            date_difference = (birthday_this_year - date_today).days

            if 0 <= date_difference <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() >= 5:
                    days_to_monday = 7 - congratulation_date.weekday()
                    congratulation_date += timedelta(days=days_to_monday)

                formatted_congratulation_date = congratulation_date.strftime("%d.%m.%Y")

                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": formatted_congratulation_date})
                
        return upcoming_birthdays
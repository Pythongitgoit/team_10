import pickle
import re
from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self._name = None
        self.name = value
        super().__init__(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        pattern = r"^[a-zA-Zа-яА-ЯІіЇї\s'\".,-]{2,}$"
        if re.match(pattern, value):
            self._name = value
        else:
            raise ValueError("Name is not correct")


class Phone(Field):
    def __init__(self, value: str):
        self._phone = None
        self.phone = value
        super().__init__(value)

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if len(value) == 10 and value.isdigit():
            self._phone = value
        else:
            raise ValueError("Number not correct")


class Birthday(Field):
    def __init__(self, value):
        self._birthday = None
        if value:
            self.birthday = value
        super().__init__(value)

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        if isinstance(value, datetime):
            self._birthday = value
        else:
            raise ValueError("Incorrect date")

    def __str__(self):
        return str(self.birthday)


class Email(Field):
    def __init__(self, value: str):
        self._email = None
        self.email = value
        super().__init__(value)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, value):
            self._email = value
        else:
            raise ValueError("Email not correct")


class AddressField:
    def __init__(self, city: str, street: str, house: str):
        self._city = None
        self._street = None
        self._house = None
        self.city = city
        self.street = street
        self.house = house

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        if value is None:
            self._city = None
        elif isinstance(value, str) and len(value) > 0:
            self._city = value
        else:
            raise ValueError("City is not valid")

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, value):
        if value is None:
            self._street = None
        elif isinstance(value, str) and len(value) > 0:
            self._street = value
        else:
            raise ValueError("Street is not valid")

    @property
    def house(self):
        return self._house

    @house.setter
    def house(self, value):
        if value is None:
            self._house = None
        elif isinstance(value, str):
            self._house = value
        else:
            raise ValueError("House number is not valid")

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}"


class Address(AddressField):
    def __init__(self, city, street, house):
        super().__init__(city, street, house)


class Record:
    def __init__(self, name: str, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.emails = []
        self.addresses = []

    def day_of_birthday(self):
        if self.birthday:
            birthday_date = self.birthday.birthday
            current_day = datetime.now()
            days_to_bd = birthday_date - current_day
            return days_to_bd.days

    def add_address(self, city, street, house):
        new_address = Address(city, street, house)
        self.addresses.append(new_address)

    def add_email(self, email):
        new_email = Email(email)
        self.emails.append(new_email)

    def add_phone(self, phone: str):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = None
        for phone in self.phones:
            if phone.value == old_phone:
                phone_to_edit = phone
                break

        if phone_to_edit is not None:
            phone_to_edit.value = new_phone
        else:
            raise ValueError("Phone not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phone_values = (
            "; ".join(p.value for p in self.phones) if self.phones else "No phone"
        )
        email_values = (
            "; ".join(e.email for e in self.emails) if self.emails else "No email"
        )
        address_values = (
            "; ".join(str(a) for a in self.addresses)
            if self.addresses
            else "No address"
        )

        return f"Contact name: {self.name.value}, phones: {phone_values}, \
               emails: {email_values}, addresses: {address_values}"


class AddressBook(UserDict):
    def add_record(self, record):
        name_value = record.name.value
        if name_value not in self.data:
            self.data[name_value] = [record]
        else:
            self.data[name_value].append(record)

    def find(self, name):
        records = self.data.get(name)
        if records:
            return records[0]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def show_birthday_contacts(self, days):
        current_date = datetime.now()
        birthday_contacts = []
        for records in self.data.values():
            for contact in records:
                if contact.birthday:
                    days_to_birthday = (contact.birthday.birthday - current_date).days
                    if 0 <= days_to_birthday <= days:
                        birthday_contacts.append(contact)
        return birthday_contacts

    def all_contacts_list(self):
        result = []
        for key, val in self.data.items():
            for record in val:
                result.append(f"{record}")
        return result

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            unpacked = pickle.load(file)
            return unpacked

    def find_contact(self, query):
        result = []
        for key, val in self.data.items():
            for record in val:
                if (
                    query in record.name.value
                    or query in [phone.value for phone in record.phones]
                    or query in [email.email for email in record.emails]
                    or query in [str(address) for address in record.addresses]
                ):
                    result.append(record)
        return result

    def __str__(self):
        result = []
        for key, val in self.data.items():
            name = key
            phone = [p for p in val]
            result.append(f"Name: {name}, other info: {phone}")
        return "\n".join(result)


class AddressBookIterator:
    def __init__(self, address_book, page_size=None):
        self.page_size = page_size
        self.address_book = address_book
        self.current_page = 0
        self.pages = []

        if page_size is not None:
            items = list(address_book.items())
            for i in range(0, len(items), page_size):
                self.pages.append(items[i : i + page_size])
        else:
            print("I dont have number of pages")

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_page < len(self.pages):
            page = self.pages[self.current_page]
            self.current_page += 1
            records = []

            for name, record_list in page:
                for record in record_list:
                    name = record.name.name
                    phones = [phone.phone for phone in record.phones]
                    records.append((name, phones))

            return records
        else:
            raise StopIteration


class Notes:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def clear(self):
        self.notes = []

    def search_note(self, keyword):
        found_notes = []
        for note in self.notes:
            if keyword.lower() in note.text.lower():
                found_notes.append(note)
        return found_notes

    def sort_notes_by_tags(self, tag):
        sorted_notes = [note for note in self.notes if tag in note.tags]
        sorted_notes.sort(key=lambda note: note.tags.index(tag))
        return sorted_notes


class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags is not None else []

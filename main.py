from datetime import datetime
import pickle
import atexit
import os

import objects
from clean import *


def save_data(address_book, notes):
    with open("address_book.pkl", "wb") as address_book_file:
        pickle.dump(address_book, address_book_file)
    with open("notes.pkl", "wb") as notes_file:
        pickle.dump(notes, notes_file)


def load_data():
    address_book = objects.AddressBook()
    notes = objects.Notes()

    if os.path.exists("address_book.pkl"):
        with open("address_book.pkl", "rb") as address_book_file:
            address_book = pickle.load(address_book_file)

    if os.path.exists("notes.pkl"):
        with open("notes.pkl", "rb") as notes_file:
            notes = pickle.load(notes_file)

    return address_book, notes


def help_func():
    print(
        """   add - Додати контакт: Ця команда дозволяє вам додати новий контакт до адресної книги. Ви вводите ім'я, номер телефону, електронну пошту (за бажанням), адресу (якщо є) та дату народження (за бажанням) для нового контакту.
                search - Пошук контакту: Ця команда дозволяє вам знайти контакти за ключовим словом. Ви вводите ключове слово, і програма виводить контакти, які містять це слово в імені, телефоні, електронній пошті або адресі.
                delete - Видалити контакт: Ця команда дозволяє вам видалити контакт з адресної книги. Ви вводите ім'я контакту, який потрібно видалити.
                add_note - Додати нотатку: Ця команда дозволяє вам додати нову нотатку до своїх нотаток. Ви вводите текст нотатки та теги (якщо є).
                search_note - Пошук нотатки: Ця команда дозволяє вам знайти нотатки за ключовим словом. Ви вводите ключове слово, і програма виводить нотатки, які містять це слово в тексті.
                sort - Сортування нотаток за тегами: Ця команда сортує ваші нотатки за тегами. Ви вводите тег, і програма виводить всі нотатки з цим тегом, впорядковані за ним.
                hello - Вивести привітання: Ця команда виводить привітання від бота.
                close - Завершити роботу: Ця команда завершує роботу програми та виводить прощання.
                clear - Видалення данних: Ця команда видаляє всі збережені данні в нотатках та адресної книги.
                sort_folder - Сортує файли у вказаній папці.Наприклад C:/Users/your_username/Desktop/trash. Використовуйте обережно. 
                help - Список всіх команд"""
    )


def add_contact(address_book):
    while True:
        name = input("Enter the contact's name: ")
        while True:
            try:
                name = objects.Name(name)
                break
            except ValueError as e:
                print(f"Error: {e}")
                name = input("Enter the contact's name: ")

        phone = input("Enter the contact's phone: ")
        while True:
            try:
                if phone:
                    phone = objects.Phone(phone)
                break
            except ValueError as e:
                print(f"Error: {e}")
                phone = input("Enter the contact's phone: ")

        email = input(
            "Enter the contact's email (if available, otherwise press Enter): "
        )
        while True:
            try:
                if email:
                    email = objects.Email(email)
                break
            except ValueError as e:
                print(f"Error: {e}")
                email = input("Enter the contact's email: ")

        address = input(
            "Enter the contact's address (if available, format input - city street house, otherwise press Enter): "
        )
        while True:
            try:
                if address:
                    new_address = address.split()
                    city, street, house = new_address
                    address = objects.Address(city, street, house)
                break
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
                address = input("Enter the contact's address: ")

        birthday = input("Enter the birthday (if available, otherwise press Enter): ")
        while True:
            try:
                if birthday:
                    birthday = datetime.strptime(birthday, "%Y-%m-%d")
                break
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
                birthday = input("Enter the birthday: ")

        contact = objects.Record(name.name, birthday)
        if phone:
            contact.add_phone(phone.phone)
        if email:
            contact.add_email(email.email)
        if address:
            city, street, house = address.city, address.street, address.house
            contact.add_address(city, street, house)
        address_book.add_record(contact)
        print(f"New contact, {name.name} successfully added")
        break


def show_contacts(address_book, page_size):
    address_book_iterator = objects.AddressBookIterator(address_book, page_size)
    result = []
    for page in address_book_iterator:
        for record in page:
            result.append(f'{record[0]}, {"; ".join(rec for rec in record[1])}')
    print(", ".join(result))


def edit_phone(address_book, contacts, name, old_phone, new_phone):
    for contact in contacts:
        if contact.name.value == name:
            for phone in contact.phones:
                if phone.value == old_phone:
                    phone.value = new_phone
                    address_book.save_to_file("address_book.pkl")
                    return
    raise ValueError("Phone not found")


def search_contact(address_book):
    query = input("Enter the search keyword: ")
    found_contacts = address_book.find_contact(query)
    if found_contacts:
        print("Found contacts:")
        for contact in found_contacts:
            contact_info = f"Name: {contact.name.value}"
            if contact.emails and contact.emails is not None:
                contact_info += (
                    f", Email: {', '.join(email.value for email in contact.emails)}"
                )
            else:
                contact_info += f", Email: N/A"
            if contact.phones and contact.phones is not None:
                contact_info += (
                    f", Phone: {', '.join(phone.value for phone in contact.phones)}"
                )
            else:
                contact_info += f", Phone: N/A"
            if contact.addresses and contact.addresses is not None:
                contact_info += f", Address: {', '.join(str(address) for address in contact.addresses)}"
            else:
                contact_info += f", Address: N/A"
            if contact.birthday and contact.birthday.birthday is not None:
                contact_info += (
                    f", Birthday: {contact.birthday.birthday.strftime('%Y-%m-%d')}"
                )
            else:
                contact_info += f", Birthday: N/A"
            print(contact_info)
    else:
        print("Contacts not found.")


def delete_contact(address_book, name):
    if name in address_book.data:
        address_book.delete(name)
        print(f"Contact '{name}' deleted.")
    else:
        print("Contact not found.")


def add_note(notes):
    text = input("Enter note text: ")
    tags = input("Enter tags (comma-separated): ").split(",")
    note = objects.Note(text, tags)
    notes.add_note(note)


def search_note(notes):
    keyword = input("Enter a keyword to search for: ")
    tag_search = input("Do you want to search by tag (yes or no)? ").lower()

    found_notes = []
    for note in notes.notes:
        if keyword.lower() in note.text.lower() and (
            not tag_search or tag_search == "no" or tag_search == "n"
        ):
            found_notes.append(note)
        elif tag_search and tag_search in ["yes", "y"] and keyword.lower() in note.tags:
            found_notes.append(note)

    if found_notes:
        print("Found notes:")
        for note in found_notes:
            print(f"Note text: {note.text}")
            print(f"Tags: {', '.join(note.tags)}")
    else:
        print("Notes not found.")


def sort_notes_by_tags(notes):
    tag = input("Enter a tag for sorting: ")
    sorted_notes = notes.sort_notes_by_tags(tag)
    if sorted_notes:
        print(f"Sorted notes by tag '{tag}':")
        for note in sorted_notes:
            print(f"Note text: {note.text}")
            print(f"Tags: {', '.join(note.tags)}")
    else:
        print(f"No notes with the tag '{tag}' found.")


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params."
        except KeyError:
            return "Unknown record_id."
        except ValueError:
            return "Error: Invalid value format."

    return inner


def hello():
    return f"Welcome to assist bot"


def clear_data(address_book, notes):
    confirmation = input(
        "Are you sure you want to clear all data? (yes or no): "
    ).lower()
    if confirmation == "yes" or confirmation == "y":
        address_book.clear()
        notes.clear()
        print("All data has been cleared.")
    else:
        print("Clearing data canceled.")


COMMANDS = {"add": add_contact, "search": search_contact, "delete": delete_contact}


def process_command(command, address_book):
    if command in COMMANDS:
        COMMANDS[command](address_book)
    else:
        print("Invalid command")


# @user_error
def main():
    address_book, notes = load_data()
    atexit.register(save_data, address_book, notes)

    while True:
        user_input = input("Enter a command: ")
        if user_input == "hello":
            print("Welcome to assist bot")

        elif user_input == "close":
            print("Good bye")
            break
        # ***Sort folder***************************************

        elif user_input == "sort_folder":
            user_directory = get_user_input()

            if user_directory is not None:
                try:
                    main_sorting_function(user_directory)
                except FileNotFoundError:
                    print("Вказаний шлях до папки не існує.")
            else:
                print("Програма сортувальник закінчив роботу.")

        # *************************************************
        elif user_input == "delete":
            name = input("Enter the contact's name to delete: ")
            delete_contact(address_book, name)
        elif user_input == "add_note":
            add_note(notes)
        elif user_input == "search_note":
            search_note(notes)
        elif user_input == "sort":
            sort_notes_by_tags(notes)
        elif user_input == "help":
            help_func()
        elif user_input == "clear":
            clear_data(address_book, notes)
        else:
            process_command(user_input, address_book)


if __name__ == "__main__":
    main()

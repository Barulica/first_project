
from models.user import insert_user
from models.db import connection
from models.book import get_all_books, insert_book
from faker import Faker
from datetime import datetime

fake= Faker()

def generate_dob():
    return fake.date_between(start_date=datetime(1950, 1, 1).date(), end_date=datetime(2010, 1, 1).date())


def display_menu():
    print("Choose an option:")
    print("1. Add a new book")
    print("2. See all books")
    choice = input("What would you like to do?  \n")
    return choice

def add_new_book(con):
    name = input("What is name of the book? \n")
    genre = input("What is genre of the book? \n")
    author_name = input("What is author of the book? \n")

    cursor = con.cursor()
    cursor.execute("SELECT id FROM users WHERE name = %s", (author_name,))
    result = cursor.fetchone()

    if result:
        author_id = result['id']
        print(f'Found author {author_name} with ID {author_id}!')

    else:
        print(f"Author '{author_name}' not found. Creating a new author."),
        author_dob = generate_dob()
        author_id = insert_user(con, author_name, author_dob)
        print(f"New author '{author_name}' added with ID {author_id}.")

    insert_book(con, name, genre, author_id)
    print(f"New book '{name}' added successfully!")

def see_all_books(con):
    books = get_all_books(con)
    if books:
        print('All books in the Database:\n')
        for book in books:
            print(f"Name: {book.name}, Genre: {book.genre}")

    else:
        print("No books found")


def main():
    while True:
        choice = display_menu()

        if choice == "1":
            add_new_book(connection)  # Add a new book
        elif choice == "2":
            see_all_books(connection)  # Display all books
        else:
            print("Invalid choice, please select 1 or 2.")

        # Ask if they want to continue or exit
        continue_choice = input("Do you want to continue? (y/n): ").lower()
        if continue_choice != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()






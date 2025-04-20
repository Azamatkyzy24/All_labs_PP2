import psycopg2, csv

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="phonebook", 
    user="postgres", 
    host="localhost", 
    password="1465", 
    port=5432
)
conn.autocommit = True

# SQL commands
command_create_table = """
    CREATE TABLE IF NOT EXISTS phonebook( 
        user_id SERIAL NOT NULL PRIMARY KEY, 
        username VARCHAR(255),
        phone_number VARCHAR(255)
    );
"""

command_insert_into_csv = 'INSERT INTO phonebook (username, phone_number) VALUES (%s, %s)'

command_update_phone = 'UPDATE phonebook SET phone_number = %s WHERE user_id = %s'

command_update_name = 'UPDATE phonebook SET username = %s WHERE user_id = %s'

command_filter_name_starts = "SELECT * FROM phonebook WHERE username LIKE %s"

command_filter_phone_starts = "SELECT * FROM phonebook WHERE phone_number LIKE %s"

command_delete_by_phone = "DELETE FROM phonebook WHERE phone_number = %s"

command_delete_by_name = "DELETE FROM phonebook WHERE username = %s"

cur = conn.cursor()

csv_file = 'C:/Users/aidan/OneDrive/Рабочий стол/lab 10-11/phones.csv'

# Ensure the table is created
cur.execute(command_create_table)

def csv_to_db(csv_file):
    """Function to insert records from CSV file."""
    with open(csv_file, 'r', encoding='utf-8-sig') as file_csv:
        reader_csv = csv.reader(file_csv, delimiter=',')
        for row in reader_csv:
            try:
                cur.execute(command_insert_into_csv, (row[0], row[1]))
            except Exception as e:
                print(f"Error inserting row {row}: {e}")

def print_rows():
    """Function to print all records from the phonebook."""
    cur.execute('SELECT * FROM phonebook')
    results = cur.fetchall()
    for row in results:
        print(row)

def insert_to_db():
    """Insert new user into phonebook."""
    username = input('Enter the username: ')
    phone = input('Enter the phone number: ')
    cur.execute(command_insert_into_csv, (username, phone))
    print("Inserted successfully!")
    print_rows()

def change_name():  
    """Update user name."""
    new_username = input("Enter the new username: ")
    user_id = int(input('Enter the ID you want to change: '))
    cur.execute(command_update_name, (new_username, user_id))
    print_rows()

def change_phone_number():
    """Update user phone number."""
    new_phone = input("Enter the new phone number: ")
    user_id = int(input('Enter the ID you want to change: '))
    cur.execute(command_update_phone, (new_phone, user_id))
    print_rows()

def filter_name_start_by():
    """Filter users by the starting letters of the name."""
    starts_with = input("Enter the letters that should start the name: ")
    cur.execute(command_filter_name_starts, (starts_with + '%',))
    results = cur.fetchall()
    for row in results:
        print(row)

def filter_phone_start_by():
    """Filter users by the starting digits of the phone number."""
    starts_with = input('Enter the digits that the phone number should start with: ')
    cur.execute(command_filter_phone_starts, (starts_with + '%',)) 
    results = cur.fetchall()
    for row in results:
        print(row)

def delete_by_phone():
    """Delete user by phone number."""
    phone_number = input('Enter the phone you want to delete: ')
    cur.execute(command_delete_by_phone, (phone_number,))
    print_rows()

def delete_by_name():
    """Delete user by name."""
    name = input('Enter the name you want to delete: ')
    cur.execute(command_delete_by_name, (name,))
    print_rows()

def get_starting_with(letter):
    """Get users whose username starts with the given letter."""
    command = 'SELECT username FROM phonebook WHERE LEFT(username, 1) = %s'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (letter,))
            result = cur.fetchall()
            print(result)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def get_user_input():
    """Display available commands and get user input."""
    commands = """    insert - Inserting into the database
    change name - Changing the name of the user by the id
    change phone number - Changing the phone number of the user by the id
    filter by name - Filtering by the name that starts with the given value
    filter by phone number - Filtering by the phone number that starts with the given value
    delete by name - Deleting record by the name 
    delete by phone number - Deleting record by the phone number
    print all - Printing all records in the table
    insert csv - Inserting all records to the database from the csv file
    start with letter - Selecting usernames starting with the given letter"""
    print(commands)
    user_input = input("Enter the command: ")
    if user_input == 'insert':
        insert_to_db()
    elif user_input == 'change name':
        change_name()
    elif user_input == 'change phone number':
        change_phone_number()
    elif user_input == 'filter by name':
        filter_name_start_by()
    elif user_input == 'filter by phone number':
        filter_phone_start_by()
    elif user_input == 'delete name':
        delete_by_name()
    elif user_input == 'delete phone number':
        delete_by_phone()
    elif user_input == 'print all':
        print_rows()
    elif user_input == 'insert csv':
        csv_to_db(csv_file)
        print_rows()
    elif user_input == 'start with letter':
        letter = input('Enter the letter: ')
        get_starting_with(letter)

get_user_input()

conn.commit()

cur.close()
conn.close()
import psycopg2
import csv

conn = psycopg2.connect(
    dbname="DataBase",
    user="postgres",
    password="A2682772aa",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    print("Table created.")

def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s)", row)
    conn.commit()
    print("Data from CSV inserted.")

def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone number: ")
    cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print("Data inserted.")

def update_data():
    username = input("Enter username to update: ")
    new_phone = input("Enter new phone number: ")
    cur.execute("UPDATE PhoneBook SET phone = %s WHERE username = %s", (new_phone, username))
    conn.commit()
    print("Data updated.")

def query_data():
    filter_name = input("Enter name to filter by: ")
    cur.execute("SELECT * FROM PhoneBook WHERE username ILIKE %s", ('%' + filter_name + '%',))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_data():
    username = input("Enter username to delete: ")
    cur.execute("DELETE FROM PhoneBook WHERE username = %s", (username,))
    conn.commit()
    print("Data deleted.")

def menu():
    while True:
        print("\n=== Menu ===")
        print("1. Create table")
        print("2. Insert data from CSV")
        print("3. Insert data from console")
        print("4. Update data")
        print("5. Query data")
        print("6. Delete data")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("phonebook/contacts.csv")
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_data()
        elif choice == "5":
            query_data()
        elif choice == "6":
            delete_data()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            
if __name__ == "__main__":
    menu()

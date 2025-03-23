import mysql.connector as sqltor
from tkinter import *

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWD = "kingkunga6799@"
DB_NAME = "per"

# Global database connection and cursor
mycon = None
mycur = None

def create_database(file_path, host, user, passwd, new_db_name):
    try:
        # Step 1: Connect to MySQL (without selecting a database yet)
        connection = sqltor.connect(host=host, user=user, passwd=passwd)
        cursor = connection.cursor()

        # Step 2: Create a new database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
        print(f"Database '{new_db_name}' created (or already exists).")

        # Step 3: Switch to the new database
        cursor.execute(f"USE {new_db_name};")
        print(f"Using '{new_db_name}' database.")

        # Step 4: Open and read the SQL file
        with open(file_path, 'r') as file:
            sql_queries = file.read()

        # Step 5: Split the SQL file content into individual queries
        queries = sql_queries.split(';')  # Split by semicolon to separate each query

        # Step 6: Execute each query from the file
        for query in queries:
            query = query.strip()  # Remove any extra whitespace
            if query:  # If the query is not empty
                cursor.execute(query)

        # Commit any changes if the SQL contains DML (Data Manipulation Language) queries
        connection.commit()

        print("SQL file executed successfully!")

    except sqltor.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def connect_to_db():
    global mycon, mycur
    try:
        mycon = sqltor.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mycon.cursor()
    except sqltor.Error as err:
        print(f"Error: {err}")

def close_db():
    global mycur, mycon
    if mycur:
        mycur.close()
    if mycon:
        mycon.close()

def a_click(n):
    master = Tk()
    master.geometry('400x500')
    master.maxsize(400, 600)
    
    try:
        connect_to_db()
        mycur.execute("SELECT name, des FROM types WHERE ano = %s", (n,))
        data = mycur.fetchone()
        
        if data:
            name, description = data
        else:
            name, description = "No data found", "No description available"
        
        Message(master, text=name, font=('Arial Bold', 20), bg='#F08080', width=300).place(x=0)
        Message(master, text=description, font=('Arial Bold', 12), width=400).pack(side='bottom')
        Button(master, text='Back', font=("Arial Bold", 9), width=10, relief="raised", command=master.destroy).place(x=320)
    
    except sqltor.Error as err:
        print(f"Error: {err}")
        Message(master, text="An error occurred while connecting to the database.", font=('Arial Bold', 20), bg='#FF6347', width=300).place(x=0)
        Button(master, text='Back', font=("Arial Bold", 9), width=10, relief="raised", command=master.destroy).place(x=320)
    
    finally:
        close_db()

def b_click(n):
    master = Tk()
    master.geometry('400x500')
    master.maxsize(400, 600)
    
    try:
        connect_to_db()
        mycur.execute("SELECT name, sym, des FROM ele WHERE ano = %s", (n,))
        data = mycur.fetchone()
        
        if data:
            name, symbol, description = data
        else:
            name, symbol, description = "No data found", "No symbol", "No description available"
        
        Message(master, text=description, font=('Arial Bold', 12), width=400).pack(side='bottom')
        Message(master, text=f"Atomic number: {n}", font=('Arial Bold', 12), width=300).place(y=100)
        Message(master, text=symbol, font=('Arial Bold', 35)).place(x=0)
        Message(master, text=name, font=('Arial Bold', 12), width=150).place(x=0, y=70)
        Button(master, text='Back', font=("Arial Bold", 9), width=10, relief="raised", command=master.destroy).place(x=320)
    
    except sqltor.Error as err:
        print(f"Error: {err}")
        Message(master, text="An error occurred while connecting to the database.", font=('Arial Bold', 20), bg='#FF6347', width=300).place(x=0)
        Button(master, text='Back', font=("Arial Bold", 9), width=10, relief="raised", command=master.destroy).place(x=320)
    
    finally:
        close_db()

def create_periodic_table(root):
    elements = [
        # Format: (text, bg_color, row, column, atomic_number)
        ('H', '#308014', 0, 0, 1), ('He', '#00C957', 0, 17, 2),
        ('Li', '#F08080', 1, 0, 3), ('Be', '#FFA500', 1, 1, 4),
        ('B', '#FFFF00', 1, 12, 5), ('C', '#308014', 1, 13, 6),
        ('N', '#308014', 1, 14, 7), ('O', '#308014', 1, 15, 8),
        ('F', '#FFBBFF', 1, 16, 9), ('Ne', '#00C957', 1, 17, 10),
        # Add more elements as needed...
    ]
    
    for text, bg_color, row, column, atomic_number in elements:
        Button(root, text=text, bg=bg_color, height=4, width=8, command=lambda n=atomic_number: b_click(n)).grid(row=row, column=column)

def main():
    root = Tk()
    root.geometry("1920x1080")
    root.title("Modern Periodic Table")
    
    Label(root, text='Modern Periodic Table', font=("Arial Bold", 40), fg='black').pack()
    
    create_periodic_table(root)
    
    file_path = "C:\\Users\\tenku\\Desktop\\Projects\\Periodic Table\\ele_data.txt"
    create_database(file_path, DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
    
    Exit = Button(root, text="EXIT", height=4, width=7, bg='red', command=root.destroy)
    Exit.pack(side='bottom')
    
    root.mainloop()

if __name__ == "__main__":
    main()
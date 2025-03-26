import mysql.connector as sqltor
from tkinter import *
import os
from functools import partial
from bs4 import BeautifulSoup

class PeriodicTableApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("Modern Periodic Table")
        
        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'passwd': 'kingkunga6799@',
            'database': 'per'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main label
        Label(self.root, text='Modern Periodic Table', font=("Arial Bold", 40), fg='black').pack()
        
        # Element groups frame
        self.create_element_groups_frame()
        
        # Periodic table elements
        self.create_periodic_elements()
        
        # Lanthanoids and Actinoids
        self.create_lanthanoids_actinoids()
        
        # Exit button
        Button(self.root, text="EXIT", height=4, width=7, bg='red', 
               command=self.root.destroy).pack(side='bottom')
    
    def create_element_groups_frame(self):
        """Create the frame with element group buttons"""
        group_frame = Frame(self.root, highlightbackground='black', highlightthickness=1)
        group_frame.place(x=600, y=92)
        
        # Group definitions with colors and names
        groups = [
            (201, 'Alkali metals', '#F08080'),
            (202, 'Alkali earth metals', '#FFA500'),
            (203, 'Lanthanoides', '#7F7FFF'),
            (204, 'Actinoids', '#5FAFD7'),
            (205, 'Transition metals', '#BFEFFF'),
            (206, 'Post-Transition metals', '#EEDFCC'),
            (207, 'Metalloids', '#FFFF00'),
            (208, 'Non-metals', '#308014'),
            (209, 'Halogen', '#FFBBFF'),
            (210, 'Noble gas', '#00C957')
        ]
        
        # Create buttons in a grid
        for i, (ano, text, color) in enumerate(groups):
            row = (i // 2) + 1
            col = (i % 2) + 1
            Button(group_frame, text=text, bg=color, font=("Arial Bold", 9), 
                  height=2, width=25, command=partial(self.show_type_info, ano)
                  ).grid(column=col, row=row)
    
    def create_periodic_elements(self):
        """Create all periodic table element buttons"""
        # Element positions and properties (x, y, atomic number, symbol, color)
        elements = [
            # Period 1
            (200, 100, 1, 'H', '#308014'),
            (1305, 100, 2, 'He', '#00C957'),
            
            # Period 2
            (200, 166, 3, 'Li', '#F08080'),
            (265, 166, 4, 'Be', '#FFA500'),
            (980, 166, 5, 'B', '#FFFF00'),
            (1045, 166, 6, 'C', '#308014'),
            (1110, 166, 7, 'N', '#308014'),
            (1175, 166, 8, 'O', '#308014'),
            (1240, 166, 9, 'F', '#FFBBFF'),
            (1305, 166, 10, 'Ne', '#00C957'),
            
            # Period 3
            (200, 232, 11, 'Na', '#F08080'),
            (265, 232, 12, 'Mg', '#FFA500'),
            (980, 232, 13, 'Al', '#EEDFCC'),
            (1045, 232, 14, 'Si', '#FFFF00'),
            (1110, 232, 15, 'P', '#308014'),
            (1175, 232, 16, 'S', '#308014'),
            (1240, 232, 17, 'Cl', '#FFBBFF'),
            (1305, 232, 18, 'Ar', '#00C957'),
            
            # Period 4
            (200, 298, 19, 'K', '#F08080'),
            (265, 298, 20, 'Ca', '#FFA500'),
            (330, 298, 21, 'Sc', '#BFEFFF'),
            (395, 298, 22, 'Ti', '#BFEFFF'),
            (460, 298, 23, 'V', '#BFEFFF'),
            (525, 298, 24, 'Cr', '#BFEFFF'),
            (590, 298, 25, 'Mn', '#BFEFFF'),
            (655, 298, 26, 'Fe', '#BFEFFF'),
            (720, 298, 27, 'Co', '#BFEFFF'),
            (785, 298, 28, 'Ni', '#BFEFFF'),
            (850, 298, 29, 'Cu', '#BFEFFF'),
            (915, 298, 30, 'Zn', '#BFEFFF'),
            (980, 298, 31, 'Ga', '#EEDFCC'),
            (1045, 298, 32, 'Ge', '#FFFF00'),
            (1110, 298, 33, 'As', '#FFFF00'),
            (1175, 298, 34, 'Se', '#308014'),
            (1240, 298, 35, 'Br', '#FFBBFF'),
            (1305, 298, 36, 'Kr', '#00C957'),
            
            # Period 5
            (200, 364, 37, 'Rb', '#F08080'),
            (265, 364, 38, 'Sr', '#FFA500'),
            (330, 364, 39, 'Y', '#BFEFFF'),
            (395, 364, 40, 'Zr', '#BFEFFF'),
            (460, 364, 41, 'Nb', '#BFEFFF'),
            (525, 364, 42, 'Mo', '#BFEFFF'),
            (590, 364, 43, 'Tc', '#BFEFFF'),
            (655, 364, 44, 'Ru', '#BFEFFF'),
            (720, 364, 45, 'Rh', '#BFEFFF'),
            (785, 364, 46, 'Pd', '#BFEFFF'),
            (850, 364, 47, 'Ag', '#BFEFFF'),
            (915, 364, 48, 'Cd', '#BFEFFF'),
            (980, 364, 49, 'In', '#EEDFCC'),
            (1045, 364, 50, 'Sn', '#EEDFCC'),
            (1110, 364, 51, 'Sb', '#FFFF00'),
            (1175, 364, 52, 'Te', '#FFFF00'),
            (1240, 364, 53, 'I', '#FFBBFF'),
            (1305, 364, 54, 'Xe', '#00C957'),
            
            # Period 6
            (200, 430, 55, 'Cs', '#F08080'),
            (265, 430, 56, 'Ba', '#FFA500'),
            (330, 430, 57, '', '#7F7FFF'),  # Placeholder for Lanthanoids
            (395, 430, 72, 'Hf', '#BFEFFF'),
            (460, 430, 73, 'Ta', '#BFEFFF'),
            (525, 430, 74, 'W', '#BFEFFF'),
            (590, 430, 75, 'Re', '#BFEFFF'),
            (655, 430, 76, 'Os', '#BFEFFF'),
            (720, 430, 77, 'Ir', '#BFEFFF'),
            (785, 430, 78, 'Pt', '#BFEFFF'),
            (850, 430, 79, 'Au', '#BFEFFF'),
            (915, 430, 80, 'Hg', '#BFEFFF'),
            (980, 430, 81, 'Tl', '#EEDFCC'),
            (1045, 430, 82, 'Pb', '#EEDFCC'),
            (1110, 430, 83, 'Bi', '#EEDFCC'),
            (1175, 430, 84, 'Po', '#FFFF00'),
            (1240, 430, 85, 'At', '#FFBBFF'),
            (1305, 430, 86, 'Rn', '#00C957'),
            
            # Period 7
            (200, 496, 87, 'Fr', '#F08080'),
            (265, 496, 88, 'Ra', '#FFA500'),
            (330, 496, 89, '', '#5FAFD7'),  # Placeholder for Actinoids
            (395, 496, 104, 'Rf', '#BFEFFF'),
            (460, 496, 105, 'Db', '#BFEFFF'),
            (525, 496, 106, 'Sg', '#BFEFFF'),
            (590, 496, 107, 'Bh', '#BFEFFF'),
            (655, 496, 108, 'Hs', '#BFEFFF'),
            (720, 496, 109, 'Mt', '#BFEFFF'),
            (785, 496, 110, 'Ds', '#BFEFFF'),
            (850, 496, 111, 'Rg', '#BFEFFF'),
            (915, 496, 112, 'Cn', '#BFEFFF'),
            (980, 496, 113, 'Nh', '#EEDFCC'),
            (1045, 496, 114, 'Fl', '#EEDFCC'),
            (1110, 496, 115, 'Mc', '#EEDFCC'),
            (1175, 496, 116, 'Lv', '#EEDFCC'),
            (1240, 496, 117, 'Ts', '#FFBBFF'),
            (1305, 496, 118, 'Og', '#00C957')
        ]
        
        for x, y, atomic_num, symbol, color in elements:
            if symbol:  # Skip placeholders
                Button(self.root, text=symbol, bg=color, height=4, width=8,
                      command=partial(self.show_element_info, atomic_num)).place(x=x, y=y)
    
    def create_lanthanoids_actinoids(self):
        """Create lanthanoids and actinoids buttons"""
        # Lanthanoids (atomic numbers 57-71)
        lanthanoids = [
            (57, 'La'), (58, 'Ce'), (59, 'Pr'), (60, 'Nd'), (61, 'Pm'),
            (62, 'Sm'), (63, 'Eu'), (64, 'Gd'), (65, 'Tb'), (66, 'Dy'),
            (67, 'Ho'), (68, 'Er'), (69, 'Tm'), (70, 'Yb'), (71, 'Lu')
        ]
        
        # Actinoids (atomic numbers 89-103)
        actinoids = [
            (89, 'Ac'), (90, 'Th'), (91, 'Pa'), (92, 'U'), (93, 'Np'),
            (94, 'Pu'), (95, 'Am'), (96, 'Cm'), (97, 'Bk'), (98, 'Cf'),
            (99, 'Es'), (100, 'Fm'), (101, 'Md'), (102, 'No'), (103, 'Lr')
        ]
        
        # Place lanthanoids
        for i, (atomic_num, symbol) in enumerate(lanthanoids):
            x = 330 + (i % 14) * 65
            y = 563
            Button(self.root, text=symbol, bg='#7F7FFF', height=4, width=8,
                  command=partial(self.show_element_info, atomic_num)).place(x=x, y=y)
        
        # Place actinoids
        for i, (atomic_num, symbol) in enumerate(actinoids):
            x = 330 + (i % 14) * 65
            y = 630
            Button(self.root, text=symbol, bg='#5FAFD7', height=4, width=8,
                  command=partial(self.show_element_info, atomic_num)).place(x=x, y=y)
    
    def show_element_info(self, atomic_num):
        """Show information about a specific element"""
        info_window = Toplevel(self.root)
        info_window.geometry('400x500')
        info_window.maxsize(400, 600)
        
        try:
            connection = sqltor.connect(**self.db_config)
            cursor = connection.cursor()
            
            # Get element data
            cursor.execute("SELECT name, sym, des FROM ele WHERE ano = %s", (atomic_num,))
            element_data = cursor.fetchone()
            
            if element_data:
                name, symbol, description = element_data
                
                # Display atomic number
                Label(info_window, text=f"Atomic number: {atomic_num}", 
                      font=('Arial Bold', 12)).place(y=100)
                
                # Display symbol (large)
                Label(info_window, text=symbol, font=('Arial Bold', 35)).place(x=0)
                
                # Display name
                Label(info_window, text=name, font=('Arial Bold', 12)).place(x=0, y=70)
                
                # Display description
                Message(info_window, text=description, font=('Arial Bold', 12), 
                       width=400).pack(side='bottom')
            else:
                Label(info_window, text="Element data not found", 
                      font=('Arial Bold', 20), bg='#FF6347', width=300).place(x=0)
        
        except sqltor.Error as err:
            Label(info_window, text=f"Database error: {err}", 
                  font=('Arial Bold', 20), bg='#FF6347', width=300).place(x=0)
        
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
        
        # Back button
        Button(info_window, text='Back', font=("Arial Bold", 9), 
              width=10, relief="raised", command=info_window.destroy).place(x=320)
    
    def show_type_info(self, type_id):
        """Show information about an element type/group"""
        info_window = Toplevel(self.root)
        info_window.geometry('400x500')
        info_window.maxsize(400, 600)
        
        try:
            connection = sqltor.connect(**self.db_config)
            cursor = connection.cursor()
            
            # Get type data
            cursor.execute("SELECT name, des FROM types WHERE ano = %s", (type_id,))
            type_data = cursor.fetchone()
            
            if type_data:
                name, description = type_data
                
                # Display type name
                Message(info_window, text=name, font=('Arial Bold', 20),
                       bg='#F08080', width=300).place(x=0)
                
                # Display description
                Message(info_window, text=description, font=('Arial Bold', 12), 
                       width=400).pack(side='bottom')
            else:
                Label(info_window, text="Type data not found", 
                      font=('Arial Bold', 20), bg='#FF6347', width=300).place(x=0)
        
        except sqltor.Error as err:
            Label(info_window, text=f"Database error: {err}", 
                  font=('Arial Bold', 20), bg='#FF6347', width=300).place(x=0)
        
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
        
        # Back button
        Button(info_window, text='Back', font=("Arial Bold", 9), 
              width=10, relief="raised", command=info_window.destroy).place(x=320)

def create_database(file_path, host, user, passwd, new_db_name):
    """Create database and execute SQL file"""
    try:
        # Connect to MySQL (without selecting a database yet)
        connection = sqltor.connect(host=host, user=user, passwd=passwd)
        cursor = connection.cursor()

        # Create a new database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
        print(f"Database '{new_db_name}' created (or already exists).")

        # Switch to the new database
        cursor.execute(f"USE {new_db_name};")
        print(f"Using '{new_db_name}' database.")

        # Read and execute SQL file
        with open(file_path, 'r') as file:
            sql_queries = file.read()

        # Execute each query
        for query in sql_queries.split(';'):
            query = query.strip()
            if query:
                cursor.execute(query)

        connection.commit()
        print("SQL file executed successfully!")

    except sqltor.Error as err:
        print(f"Error: {err}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def main():
    root = Tk()
    app = PeriodicTableApp(root)
    
    # Initialize database (adjust path as needed)
    sql_file_path = "ele_data.txt"  # Update this path
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'passwd': 'kingkunga6799@',
        'database': 'per'
    }
    
    create_database(sql_file_path, **db_config)
    
    root.mainloop()

if __name__ == "__main__":
    main()
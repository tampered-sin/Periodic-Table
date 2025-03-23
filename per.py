import mysql.connector as sqltor
from tkinter import *
import os

root = Tk()
root.geometry("1920x1080")
mycon = ''
mycur = ''


def create_database(file_path, host, user, passwd, new_db_name):
    try:
        # Step 1: Connect to MySQL (without selecting a database yet)
        connection = sqltor.connect(
            host=host,
            user=user,
            passwd=passwd
        )
        cursor = connection.cursor()

        # Step 2: Create a new database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
        print(f"Database '{new_db_name}' created (or already exists).")

        # Step 3: Switch to the new database
        cursor.execute(f"USE {new_db_name};")
        print(f"using '{new_db_name}' database.")

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


# For Types
def a_click(n):
    global mycon
    global mycur
    
    # Create a new window
    master = Tk()
    master.geometry('400x500')
    master.maxsize(400,600) 
    
    try:
        # Connect to MySQL
        mycon = sqltor.connect(
            host='localhost', 
            user='root',
            passwd='kingkunga6799@',
            database='per'
        )
        mycur = mycon.cursor()
        
        # Query for element name
        q = "SELECT name FROM types WHERE ano = %s" % n
        mycur.execute(q)
        data = mycur.fetchone()
        
        if data:  # Check if data was returned
            data = data[0]
        else:
            data = "No data found"
        
        # Query for element description
        a = "SELECT des FROM types WHERE ano = %s" % n
        mycur.execute(a)
        description = mycur.fetchone()
        
        if description:  # Check if description was returned
            description = description[0]
        else:
            description = "No description available"
        
        # Display the name in the Message widget
        messageVar1 = Message(master, text=data, font=('Arial Bold', 20),
                              bg='#F08080', width=300)
        messageVar1.place(x=0)
        
        # Display the description
        messageVar2 = Message(master, text=description, font=('Arial Bold', 12), width=400)
        messageVar2.pack(side='bottom')

        # Back button to close the window
        bexit = Button(master, text='Back', font=("Arial Bold", 9), width=10, relief="raised", command=master.destroy)
        bexit.place(x=320)
    
    except sqltor.Error as err:
        print(f"Error: {err}")
        error_message = "An error occurred while connecting to the database."
        messageVar1 = Message(master, text=error_message, font=('Arial Bold', 20),
                              bg='#FF6347', width=300)
        messageVar1.place(x=0)
        bexit = Button(master, text='Back', font=("Arial Bold", 9), width=10, relief="raised", command=master.destroy)
        bexit.place(x=320)
    
    finally:
        # Ensure that the connection and cursor are closed
        if mycur:
            mycur.close()
        if mycon:
            mycon.close()


# For Elements
def b_click(n):
    global data
    master = Tk()
    master.geometry('400x500')
    master.maxsize(400,600) 
    global mycon
    global mycur

    try:
        mycon = sqltor.connect(
            host='localhost', 
            user='root',
            passwd='kingkunga6799@',
            database='per'
        )
        mycur = mycon.cursor()
        q = "select * from ele where ano = %s" %n
        mycur.execute(q)
        data = mycur.fetchone()[2]
        a = "select sym from ele where ano = %s" %n
        mycur.execute(a)
        a1 = mycur.fetchone()[0]
        q2 = "select name from ele where ano = %s"%n
        mycur.execute(q2)
        name = mycur.fetchone()
        messageVar1 = Message(master, text = data,
                            font =('Arial Bold',12),width=400)
        messageVar1.pack(side='bottom')
        c = 'Atomic number : '
        messageVar2 = Message(master, text = (c+str(n)),
                            font =('Arial Bold',12),width=300)
        messageVar2.place(y=100)
        
        messageVar3 = Message(master, text = a1,
                            font =('Arial Bold',35))
        messageVar3.place(x=0)
        messageVar4 = Message(master, text = name,
                            font =('Arial Bold',12),width=150)
        messageVar4.place(x=0,y=70)
        bexit = Button(master,text = 'Back',font=("Arial Bold",9), 
                width=10,relief="raised",command = master.destroy)
        bexit.place(x=320)
    except sqltor.Error as err:
        print(f"Error: {err}")
        error_message = "An error occurred while connecting to the database."
        messageVar1 = Message(master, text=error_message, font=('Arial Bold', 20),
                              bg='#FF6347', width=300)
        messageVar1.place(x=0)
        bexit = Button(master, text='Back', font=("Arial Bold", 9), width=10, relief="raised", command=master.destroy)
        bexit.place(x=320)
    
    finally:
        # Ensure that the connection and cursor are closed
        if mycur:
            mycur.close()
        if mycon:
            mycon.close()
    
l1 = Label(root,text = 'Modern Periodic Table',
           font=("Arial Bold", 40),fg='black')
l1.pack()
    

    
F1 = Frame(root,highlightbackground = 'black',highlightthickness=1)
F1.place(x=600,y= 92)
g1 = Button(F1,text = 'Alkali metals',bg = '#F08080',
            font=("Arial Bold",9), height=2,width=25,
            command = lambda: a_click(201)).grid(column=1,row=1)
g2= Button(F1,text = 'Alkali earth metals',bg='#FFA500',
           font=("Arial Bold",9), height=2,width=25,
           command = lambda: a_click(202)).grid(column=2,row=1)
g3= Button(F1,text = 'Lanthanoides',bg = '#7F7FFF',
           font=("Arial Bold",9),height=2,width=25,
           command = lambda: a_click(203)).grid(column=1,row=2)
g4= Button(F1,text = 'Actinoids',bg = '#5FAFD7',
           font=("Arial Bold",9),height=2,width=25,
           command = lambda: a_click(204)).grid(column=2,row=2)
g5= Button(F1,text = 'Transition metals',bg='#BFEFFF',
           font=("Arial Bold",9),height=2,width=25,
           command = lambda: a_click(205)).grid(column=1,row=3)
g6= Button(F1,text = 'Post-Transition metals',bg='#EEDFCC',
           font=("Arial Bold",9),height=2,width=25,
           command = lambda: a_click(206)).grid(column=2,row=3)
g7= Button(F1,text = 'Metalloids',bg='#FFFF00',
           font=("Arial Bold",9),height=2,width=25,
           command = lambda: a_click(207)).grid(column=1,row=4)
g8= Button(F1,text = 'Non-metals',bg='#308014',
           font=("Arial Bold",9),height=2,width=25,
           command = lambda: a_click(208)).grid(column=2,row=4)
g9= Button(F1,text = 'Halogen',bg='#FFBBFF',
           font=("Arial Bold",9),height=2,width=25,
           command = lambda: a_click(209)).grid(column=1,row=5)
g10= Button(F1,text = 'Noble gas',bg='#00C957',
            font=("Arial Bold",9),height=2,width=25,
            command = lambda: a_click(210)).grid(column=2,row=5)


b1 = Button(root, text = 'H' ,bg='#308014',height=4,width = 8,
            command = lambda: b_click(1) ).place(x=200,y=100)
b2 = Button(root, text = 'He' ,bg='#00C957',height=4,width = 8,
            command = lambda: b_click(2) ).place(x=1305,y=100)
b3 = Button(root, text = 'Li' ,bg='#F08080',height=4,width = 8,
            command = lambda: b_click(3) ).place(x=200,y=166)
b4 = Button(root, text = 'Be' ,bg='#FFA500',height=4,width = 8,
            command = lambda: b_click(4) ).place(x=265,y=166)
b5 = Button(root, text = 'B' ,bg='#FFFF00',height=4,width = 8,
            command = lambda: b_click(5) ).place(x=980,y=166)
b6 = Button(root, text = 'C' ,bg='#308014',height=4,width = 8,
            command = lambda: b_click(6) ).place(x=1045,y=166)
b7 = Button(root, text = 'N' ,bg='#308014',height=4,width = 8,
            command = lambda: b_click(7) ).place(x=1110,y=166)
b8 = Button(root, text = 'O' ,bg='#308014',height=4,width = 8,
            command = lambda: b_click(8) ).place(x=1175,y=166)
b9 = Button(root, text = 'F' ,bg='#FFBBFF',height=4,width = 8,
            command = lambda: b_click(9) ).place(x=1240,y=166)
b10 = Button(root, text = 'Ne' ,bg='#00C957',height=4,width = 8,
             command = lambda: b_click(10) ).place(x=1305,y=166)
b11 = Button(root, text = 'Na' ,bg='#F08080',height=4,width = 8,
             command = lambda: b_click(11) ).place(x=200,y=232)
b12 = Button(root, text = 'Mg' ,bg='#FFA500',height=4,width = 8,
             command = lambda: b_click(12) ).place(x=265,y=232)
b13 = Button(root, text = 'Al' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(13) ).place(x=980,y=232)
b14 = Button(root, text = 'Si' ,bg='#FFFF00',height=4,width = 8,
             command = lambda: b_click(14) ).place(x=1045,y=232)
b15 = Button(root, text = 'P' ,bg='#308014',height=4,width = 8,
             command = lambda: b_click(15) ).place(x=1110,y=232)
b16 = Button(root, text = 'S' ,bg='#308014',height=4,width = 8,
             command = lambda: b_click(16) ).place(x=1175,y=232)


b17 = Button(root, text = 'Cl' ,bg='#FFBBFF',height=4,width = 8,
             command = lambda: b_click(17) ).place(x=1240,y=232)
b18 = Button(root, text = 'Ar' ,bg='#00C957',height=4,width = 8,
             command = lambda: b_click(18) ).place(x=1305,y=232)
b19 = Button(root, text = 'K' ,bg='#F08080',height=4,width = 8,
             command = lambda: b_click(19) ).place(x=200,y=298)
b20 = Button(root, text = 'Ca' ,bg='#FFA500',height=4,width = 8,
             command = lambda: b_click(20) ).place(x=265,y=298)
b21 = Button(root, text = 'Sc' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(21) ).place(x=330,y=298)
b22 = Button(root, text = 'Ti' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(22) ).place(x=395,y=298)
b23 = Button(root, text = 'V' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(23) ).place(x=460,y=298)
b24 = Button(root, text = 'Cr' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(24) ).place(x=525,y=298)
b25 = Button(root, text = 'Mn' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(25) ).place(x=590,y=298)
b26 = Button(root, text = 'Fe' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(26) ).place(x=655,y=298)
b27 = Button(root, text = 'Co' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(27) ).place(x=720,y=298)
b28 = Button(root, text = 'Ni' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(28) ).place(x=785,y=298)
b29 = Button(root, text = 'Cu' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(29) ).place(x=850,y=298)
b30 = Button(root, text = 'Zn' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(30) ).place(x=915,y=298)
b31 = Button(root, text = 'Ga' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(31) ).place(x=980,y=298)
b32 = Button(root, text = 'Ge' ,bg='#FFFF00',height=4,width = 8,
             command = lambda: b_click(32) ).place(x=1045,y=298)


b33 = Button(root, text = 'As' ,bg='#FFFF00',height=4,width = 8,
             command = lambda: b_click(33) ).place(x=1110,y=298)
b34 = Button(root, text = 'Se' ,bg='#308014',height=4,width = 8,
             command = lambda: b_click(34) ).place(x=1175,y=298)
b35 = Button(root, text = 'Br' ,bg='#FFBBFF',height=4,width = 8,
             command = lambda: b_click(35) ).place(x=1240,y=298)
b36 = Button(root, text = 'Kr' ,bg='#00C957',height=4,width = 8,
             command = lambda: b_click(36) ).place(x=1305,y=298)
b37 = Button(root, text = 'Rb' ,bg='#F08080',height=4,width = 8,
             command = lambda: b_click(37) ).place(x=200,y=364)
b38 = Button(root, text = 'Sr' ,bg='#FFA500',height=4,width = 8,
             command = lambda: b_click(38) ).place(x=265,y=364)
b39 = Button(root, text = 'Y' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(39) ).place(x=330,y=364)
b40 = Button(root, text = 'Zr' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(40) ).place(x=395,y=364)
b41 = Button(root, text = 'Nb' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(41) ).place(x=460,y=364)
b42 = Button(root, text = 'Mo' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(42) ).place(x=525,y=364)
b43 = Button(root, text = 'Tc' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(43) ).place(x=590,y=364)
b44 = Button(root, text = 'Ru' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(44) ).place(x=655,y=364)
b45 = Button(root, text = 'Rh' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(45) ).place(x=720,y=364)
b46 = Button(root, text = 'Pd' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(46) ).place(x=785,y=364)
b47 = Button(root, text = 'Ag' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(47) ).place(x=850,y=364)
b48 = Button(root, text = 'Cd' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(48) ).place(x=915,y=364)


b49 = Button(root, text = 'In' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(49) ).place(x=980,y=364)
b50 = Button(root, text = 'Sn' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(50) ).place(x=1045,y=364)
b51 = Button(root, text = 'Sb' ,bg='#FFFF00',height=4,width = 8,
             command = lambda: b_click(51) ).place(x=1110,y=364)
b52 = Button(root, text = 'Te' ,bg='#FFFF00',height=4,width = 8,
             command = lambda: b_click(52) ).place(x=1175,y=364)
b53 = Button(root, text = 'I' ,bg='#FFBBFF',height=4,width = 8,
             command = lambda: b_click(53) ).place(x=1240,y=364)
b54 = Button(root, text = 'Xe' ,bg='#00C957',height=4,width = 8,
             command = lambda: b_click(54) ).place(x=1305,y=364)
b55 = Button(root, text = 'Cs' ,bg='#F08080',height=4,width = 8,
             command = lambda: b_click(55) ).place(x=200,y=430)
b56 = Button(root, text = 'Ba' ,bg='#FFA500',height=4,width = 8,
             command = lambda: b_click(56) ).place(x=265,y=430)
b57 = Button(root, text = '' ,bg = '#7F7FFF',
             height=4,width = 8).place(x=330,y=430)
b58 = Button(root, text = 'Hf' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(72) ).place(x=395,y=430)
b59 = Button(root, text = 'Ta' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(73) ).place(x=460,y=430)
b60 = Button(root, text = 'W' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(74) ).place(x=525,y=430)
b61 = Button(root, text = 'Re' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(75) ).place(x=590,y=430)
b62 = Button(root, text = 'Os' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(76) ).place(x=655,y=430)
b63 = Button(root, text = 'Ir' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(77) ).place(x=720,y=430)
b64 = Button(root, text = 'Pt' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(78) ).place(x=785,y=430)


b65 = Button(root, text = 'Au' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(79) ).place(x=850,y=430)
b66 = Button(root, text = 'Hg' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(80) ).place(x=915,y=430)
b67 = Button(root, text = 'Ti' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(81) ).place(x=980,y=430)
b68 = Button(root, text = 'Pb' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(82) ).place(x=1045,y=430)
b69 = Button(root, text = 'Bi' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(83) ).place(x=1110,y=430)
b70 = Button(root, text = 'Po' ,bg='#FFFF00',height=4,width = 8,
             command = lambda: b_click(84) ).place(x=1175,y=430)
b71 = Button(root, text = 'At' ,bg='#FFBBFF',height=4,width = 8,
             command = lambda: b_click(85) ).place(x=1240,y=430)
b72 = Button(root, text = 'Rn' ,bg='#00C957',height=4,width = 8,
             command = lambda: b_click(86) ).place(x=1305,y=430)
b73 = Button(root, text = 'Fr' ,bg='#F08080',height=4,width = 8,
             command = lambda: b_click(87) ).place(x=200,y=496)
b74 = Button(root, text = 'Ra' ,bg='#FFA500',height=4,width = 8,
             command = lambda: b_click(88) ).place(x=265,y=496)
b75 = Button(root, text = '',bg = '#5FAFD7',
             height=4,width = 8).place(x=330,y=496)
b76 = Button(root, text = 'Rf' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(104) ).place(x=395,y=496)
b76 = Button(root, text = 'Db' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(105) ).place(x=460,y=496)
b78 = Button(root, text = 'Sg' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(106) ).place(x=525,y=496)
b79 = Button(root, text = 'Bh' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(107) ).place(x=590,y=496)
b80 = Button(root, text = 'Hs' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(108) ).place(x=655,y=496)


b81 = Button(root, text = 'Mt' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(109) ).place(x=720,y=496)
b82 = Button(root, text = 'Ds' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(110) ).place(x=785,y=496)
b83 = Button(root, text = 'Rg' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(111) ).place(x=850,y=496)
b84 = Button(root, text = 'Cn' ,bg='#BFEFFF',height=4,width = 8,
             command = lambda: b_click(112) ).place(x=915,y=496)
b85 = Button(root, text = 'Nh' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(113) ).place(x=980,y=496)
b86 = Button(root, text = 'Fl' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(114) ).place(x=1045,y=496)
b87 = Button(root, text = 'Mc' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(115) ).place(x=1110,y=496)
b88 = Button(root, text = 'Lv' ,bg='#EEDFCC',height=4,width = 8,
             command = lambda: b_click(116) ).place(x=1175,y=496)
b89 = Button(root, text = 'Ts' ,bg='#FFBBFF',height=4,width = 8,
             command = lambda: b_click(117) ).place(x=1240,y=496)
b90 = Button(root, text = 'Og' ,bg='#00C957',height=4,width = 8,
             command = lambda: b_click(118) ).place(x=1305,y=496)


    
    # Buttons for lanthanoids
l1 = Button(root, text = 'La' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(57) ).place(x=330,y=563)
l2 = Button(root, text = 'Ce' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(58) ).place(x=395,y=563)
l3 = Button(root, text = 'Pr' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(59) ).place(x=460,y=563)
l4 = Button(root, text = 'Nd' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(60) ).place(x=525,y=563)


l5 = Button(root, text = 'Pm' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(61) ).place(x=590,y=563)
l6 = Button(root, text = 'Sm' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(62) ).place(x=655,y=563)
l7 = Button(root, text = 'Eu' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(63) ).place(x=720,y=563)
l8 = Button(root, text = 'Gd' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(64) ).place(x=785,y=563)
l9 = Button(root, text = 'Tb' ,bg = '#7F7FFF',height=4,width = 8,
            command = lambda: b_click(65) ).place(x=850,y=563)
l10 = Button(root, text = 'Dy' ,bg = '#7F7FFF',height=4,width = 8,
             command = lambda: b_click(66) ).place(x=915,y=563)
l11 = Button(root, text = 'Ho' ,bg = '#7F7FFF',height=4,width = 8,
             command = lambda: b_click(67) ).place(x=980,y=563)
l12 = Button(root, text = 'Er' ,bg = '#7F7FFF',height=4,width = 8,
             command = lambda: b_click(68) ).place(x=1045,y=563)
l13 = Button(root, text = 'Tm' ,bg = '#7F7FFF',height=4,width = 8,
             command = lambda: b_click(69) ).place(x=1110,y=563)
l14 = Button(root, text = 'Yb' ,bg = '#7F7FFF',height=4,width = 8,
             command = lambda: b_click(70) ).place(x=1175,y=563)
l15 = Button(root, text = 'Lu' ,bg = '#7F7FFF',height=4,width = 8,
             command = lambda: b_click(71) ).place(x=1240,y=563)
    
# Button for actinoids

a1 = Button(root, text = 'Ac' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(89) ).place(x=330,y=630)
a2 = Button(root, text = 'Th' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(90) ).place(x=395,y=630)
a3 = Button(root, text = 'Pa' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(91) ).place(x=460,y=630)


a4 = Button(root, text = 'U' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(92) ).place(x=525,y=630)
a5 = Button(root, text = 'Np' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(93) ).place(x=590,y=630)
a6 = Button(root, text = 'Pu' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(94) ).place(x=655,y=630)
a7 = Button(root, text = 'Am' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(95) ).place(x=720,y=630)
a8 = Button(root, text = 'Cm' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(96) ).place(x=785,y=630)
a9 = Button(root, text = 'Bk' ,bg = '#5FAFD7',height=4,width = 8,
            command = lambda: b_click(97) ).place(x=850,y=630)
a10 = Button(root, text = 'Cf' ,bg = '#5FAFD7',height=4,width = 8,
             command = lambda: b_click(98) ).place(x=915,y=630)
a11 = Button(root, text = 'Es' ,bg = '#5FAFD7',height=4,width = 8,
             command = lambda: b_click(99) ).place(x=980,y=630)
a12 = Button(root, text = 'Fm' ,bg = '#5FAFD7',height=4,width = 8,
             command = lambda: b_click(100) ).place(x=1045,y=630)
a13 = Button(root, text = 'Md' ,bg = '#5FAFD7',height=4,width = 8,
             command = lambda: b_click(101) ).place(x=1110,y=630)
a14 = Button(root, text = 'No' ,bg = '#5FAFD7',height=4,width = 8,
             command = lambda: b_click(102) ).place(x=1175,y=630)
a15 = Button(root, text = 'Lr' ,bg = '#5FAFD7',height=4,width = 8,
             command = lambda: b_click(103) ).place(x=1240,y=630)
    
Exit = Button(root,text = "EXIT",height=4,width = 7,bg = 'red',
              command = root.destroy).pack(side='bottom')





file_path = "C:\\Users\\tenku\Desktop\Projects\Periodic Table\ele_data.txt"  # Path to the SQL file
host = "localhost"  # MySQL host (default is localhost)
user = "root"  # MySQL username
passwd = "kingkunga6799@"  # MySQL password
new_db_name = "per"

# Call the function to create the database and execute SQL file
create_database(file_path, host, user, passwd, new_db_name)

root.mainloop()
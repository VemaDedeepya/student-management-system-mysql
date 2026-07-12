import mysql.connector

#       Database connection

connection = mysql.connector.connect(
    host = "localhost",
    user = "****",
    password = "*****"
) 

cursor = connection.cursor()

#       Database creation


#       Table creation

create_query = '''CREATE TABLE if not exists students(
        std_id int PRIMARY KEY,
        name VARCHAR(50),
        age int,
        marks int,
        phone_no varchar(15),
        department varchar(20)
        );''' 

cursor.execute(create_query)
connection.commit()

print('Database and table are ready.')


#       Adding of a student

def add_student():
    try:
        student_id = int(input('Student Id: '))
    except ValueError:
        print("Enter valid numeric values")
        return

    name = input('Name: ') 

    try:
        age = int(input('Age: '))    
    except ValueError:
        print("Enter valid age")
        return

    try:
        marks = int(input('Marks: '))
        if marks <0 or marks > 100:
            print('Marks must be between 0 and 100')
            return    
    except ValueError:
        print("Enter valid marks")
        return

    try:
        phone_no = input('Mobile Number: ')    
        if not phone_no.isdigit() or len(phone_no) != 10:
            print("Enter a valid 10-digit mobile number.")
            return 
    except ValueError:
        print("Enter valid mobile.no")
        return
    
    
    department = input("Department: ")    
    

    insert_student = '''INSERT INTO students(std_id, name, age, marks, phone_no, department) VALUES (%s,%s,%s,%s,%s,%s)'''     
    values = (student_id,name,age,marks,phone_no,department)
    try:
        cursor.execute(insert_student, values)
        connection.commit()
        print('Student added successfully.')

    except mysql.connector.IntegrityError:
        print('Student ID already exists.')

    except mysql.connector.Error as e:
        print('Database error:', e)      

#       Displaying the student details

def display_student(row):

     print(f'''
                Id: {row[0]}
                Name: {row[1]}
                Age: {row[2]}
                Marks: {row[3]}
                Phone_no: {row[4]}
                Department: {row[5]}
                ---------------------
              ''')

#       View a student

def view_students():

    cursor.execute('SELECT * FROM students;')
    rows = cursor.fetchall()  
    if rows:
        for row in rows: 
           display_student(row)
    else:
        print('No student record found.')

#       Searching of a student

def search_student():

    try: 
        student_id = int(input('Enter the id of student you want to search: '))

    except ValueError:
        print('Student id must be an integer')
        return

    query = 'SELECT * FROM students where std_id = %s'
    values = (student_id,)
    
    cursor.execute(query,values)
    row = cursor.fetchone()
    
    if row:
        display_student(row)

    else:
        print('No student found.')
                              
#       Updating  student

def update_student():

    try: 
        student_id = int(input('Enter the id of student you want to search: '))

    except ValueError:
        print('Enter valid input ')
        return

    cursor.execute('SELECT * FROM students WHERE std_id = %s', (student_id,))
    row = cursor.fetchone()

    if not row:
        print('Student not found.')
        return


    change = input('\n Enter the column name  you want to update (name, age, marks, phone_no, department): ').lower()
    allowed = ['name', 'age', 'marks', 'phone_no', 'department']
    
    if change not in allowed:
        print('Enter a valid column name.')
        return
    
    if change == "marks":
        if update < 0 or update > 100:
            print("Marks must be between 0 and 100.")
            return

    update = input(f'Enter the updated {change}: ')

    if change in ['age', 'marks']:
        try:
            update = int(update)
        except ValueError:
            print(f'{change} must be a number.')
            return

    query = f'UPDATE students  SET {change} = %s WHERE std_id = %s'
    values = (update,student_id)
    
    cursor.execute(query,values)
    connection.commit()

    print("\nStudent updated successfully.\n")  

    cursor.execute('SELECT * FROM students WHERE std_id = %s', (student_id,))
    row = cursor.fetchone()

    display_student(row)

#       Deleting a student
 
def delete_student():
    
    try: 
        student_id = int(input('Enter the id of student you want to search: '))

    except ValueError:
        print('Enter valid input ')
        return

    cursor.execute('SELECT * FROM students WHERE std_id = %s', (student_id,))
    row = cursor.fetchone()

    if not row:
        print('Student not found.')
        return
    
    confirm = input(f'''Are you sure you want to delete student '{row[1]}' (ID: {row[0]})? (Y/N): ''').upper()

    if confirm == 'Y':
        cursor.execute('DELETE FROM students where std_id = %s', (student_id,))
        connection.commit()
        print('Student deleted successfully.')
    elif confirm == 'N': 
        print('Deletion cancelled.')    
    else:
        print('Invalid choice')

#       Asking the user's choice

while True:

    print('''========== Student Management System ==========
                1. Add Student
                2. View Students
                3. Search Student
                4. Update Student
                5. Delete Student
                6. Exit
             ===============================================
          ''' )

    try:
        choice = int(input('Choose the operation you want to perform (1,2,3,4,5,6): '))

    except ValueError:
        print('Enter valid input')
        continue

    if choice == 1:
        add_student()

    elif choice == 2:
        view_students()

    elif choice == 3:
        search_student()

    elif choice == 4:
        update_student()

    elif choice == 5:
        delete_student()

    elif choice == 6:
        print('Exiting')
        break
    else:
        print('Invalid choice!!')

cursor.close()
connection.close()
print('Database connection closed.')

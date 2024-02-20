import tkinter as tk
from tkinter import messagebox
import pymysql
import csv

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='placement_management_system'
        )

    def register_user(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO user (Username, Password, UserType) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, password, 'user'))
                self.connection.commit()
                messagebox.showinfo("Success", "User registered successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def login(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM user WHERE Username = %s AND Password = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Success", "Login successful.")
                    return result
                else:
                    messagebox.showerror("Error", "Invalid username or password.")
                    return None
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_user_details(self, username):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM user WHERE Username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                messagebox.showinfo("User Details", f"User details: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_student_details(self, usn, first_name, last_name, contact_number, email, department, graduation_year):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO student (USN, FirstName, LastName, ContactNumber, Email, Department, GraduationYear) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (usn, first_name, last_name, contact_number, email, department, graduation_year))
                self.connection.commit()
                messagebox.showinfo("Success", "Student details inserted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_gpa_details(self, usn, academic_year, semester, cumulative_gpa):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO gpa (USN, AcademicYear, Semester, CumulativeGPA) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (usn, academic_year, semester, cumulative_gpa))
                self.connection.commit()
                messagebox.showinfo("Success", "GPA details inserted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_all_tables(self):
        try:
            with self.connection.cursor() as cursor:
                tables = ['company', 'gpa', 'job', 'student', 'user']
                for table in tables:
                    sql = f"SELECT * FROM {table}"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    messagebox.showinfo(f"{table.capitalize()} Table", f"Table data: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_eligible_students(self, graduation_year):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM student WHERE GraduationYear = %s"
                cursor.execute(sql, (graduation_year,))
                eligible_students = cursor.fetchall()
                with open(f'eligible_students_{graduation_year}.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['USN', 'First Name', 'Last Name', 'Contact Number', 'Email', 'Department', 'Graduation Year'])
                    writer.writerows(eligible_students)
                messagebox.showinfo("Success", f"Eligible students for graduation year {graduation_year} exported to 'eligible_students_{graduation_year}.csv'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Placement Management System")
        self.geometry("400x300")
        
        self.db = Database()
        self.user_info = None
        
        self.create_widgets()
    
    def create_widgets(self):
        self.label = tk.Label(self, text="Welcome to Placement Management System", pady=10)
        self.label.pack()

        self.choice_var = tk.StringVar()

        self.choices = [
            "Register",
            "Login",
            "View Details",
            "Insert Student Details",
            "Insert GPA Details",
            "View All Tables",
            "Export Eligible Students",
            "Exit"
        ]

        for idx, choice in enumerate(self.choices, start=1):
            rb = tk.Radiobutton(self, text=choice, variable=self.choice_var, value=str(idx))
            rb.pack(anchor=tk.W)
        
        self.submit_button = tk.Button(self, text="Submit", command=self.handle_choice)
        self.submit_button.pack(pady=10)

    def handle_choice(self):
        choice = self.choice_var.get()

        if choice == "1":
            self.register_window()
        elif choice == "2":
            self.login_window()
        elif choice == "3":
            self.db.fetch_user_details(self.user_info[0]) if self.user_info else messagebox.showerror("Error", "Please login first.")
        elif choice == "4":
            self.insert_student_details_window()
        elif choice == "5":
            self.insert_gpa_details_window()
        elif choice == "6":
            self.db.view_all_tables()
        elif choice == "7":
            self.export_eligible_students_window()
        elif choice == "8":
            self.quit()

    def register_window(self):
        register_window = RegisterWindow(self, self.db)

    def login_window(self):
        login_window = LoginWindow(self, self.db)

    def insert_student_details_window(self):
        insert_student_window = InsertStudentWindow(self, self.db)

    def insert_gpa_details_window(self):
        insert_gpa_window = InsertGPAWindow(self, self.db)

    def export_eligible_students_window(self):
        export_eligible_students_window = ExportEligibleStudentsWindow(self, self.db)


class RegisterWindow(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.title("Register")
        self.geometry("300x200")

        self.master = master
        self.db = db

        self.label = tk.Label(self, text="Register Form", pady=10)
        self.label.pack()

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(self, text="Register", command=self.register_user)
        self.submit_button.pack(pady=10)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.db.register_user(username, password)
        self.destroy()

class LoginWindow(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.title("Login")
        self.geometry("300x200")

        self.master = master
        self.db = db

        self.label = tk.Label(self, text="Login Form", pady=10)
        self.label.pack()

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(self, text="Login", command=self.login_user)
        self.submit_button.pack(pady=10)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_info = self.db.login(username, password)
        if user_info:
            self.master.user_info = user_info
        self.destroy()

class InsertStudentWindow(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.title("Insert Student Details")
        self.geometry("400x300")

        self.master = master
        self.db = db

        self.label = tk.Label(self, text="Insert Student Details", pady=10)
        self.label.pack()

        # Add entry fields for student details
        self.usn_label = tk.Label(self, text="USN:")
        self.usn_label.pack()
        self.usn_entry = tk.Entry(self)
        self.usn_entry.pack()

        self.first_name_label = tk.Label(self, text="First Name:")
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.pack()

        self.last_name_label = tk.Label(self, text="Last Name:")
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.pack()

        self.contact_number_label = tk.Label(self, text="Contact Number:")
        self.contact_number_label.pack()
        self.contact_number_entry = tk.Entry(self)
        self.contact_number_entry.pack()

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.department_label = tk.Label(self, text="Department:")
        self.department_label.pack()
        self.department_entry = tk.Entry(self)
        self.department_entry.pack()

        self.graduation_year_label = tk.Label(self, text="Graduation Year:")
        self.graduation_year_label.pack()
        self.graduation_year_entry = tk.Entry(self)
        self.graduation_year_entry.pack()

        self.submit_button = tk.Button(self, text="Insert", command=self.insert_student_details)
        self.submit_button.pack(pady=10)

    def insert_student_details(self):
        usn = self.usn_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        contact_number = self.contact_number_entry.get()
        email = self.email_entry.get()
        department = self.department_entry.get()
        graduation_year = self.graduation_year_entry.get()
        self.db.insert_student_details(usn, first_name, last_name, contact_number, email, department, graduation_year)
        self.destroy()

class InsertGPAWindow(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.title("Insert GPA Details")
        self.geometry("300x200")

        self.master = master
        self.db = db

        self.label = tk.Label(self, text="Insert GPA Details", pady=10)
        self.label.pack()

        self.usn_label = tk.Label(self, text="USN:")
        self.usn_label.pack()
        self.usn_entry = tk.Entry(self)
        self.usn_entry.pack()

        self.academic_year_label = tk.Label(self, text="Academic Year:")
        self.academic_year_label.pack()
        self.academic_year_entry = tk.Entry(self)
        self.academic_year_entry.pack()

        self.semester_label = tk.Label(self, text="Semester:")
        self.semester_label.pack()
        self.semester_entry = tk.Entry(self)
        self.semester_entry.pack()

        self.cumulative_gpa_label = tk.Label(self, text="Cumulative GPA:")
        self.cumulative_gpa_label.pack()
        self.cumulative_gpa_entry = tk.Entry(self)
        self.cumulative_gpa_entry.pack()

        self.submit_button = tk.Button(self, text="Insert", command=self.insert_gpa_details)
        self.submit_button.pack(pady=10)

    def insert_gpa_details(self):
        usn = self.usn_entry.get()
        academic_year = self.academic_year_entry.get()
        semester = self.semester_entry.get()
        cumulative_gpa = self.cumulative_gpa_entry.get()
        self.db.insert_gpa_details(usn, academic_year, semester, cumulative_gpa)
        self.destroy()

class ExportEligibleStudentsWindow(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.title("Export Eligible Students")
        self.geometry("300x200")

        self.master = master
        self.db = db

        self.label = tk.Label(self, text="Export Eligible Students", pady=10)
        self.label.pack()

        self.graduation_year_label = tk.Label(self, text="Graduation Year:")
        self.graduation_year_label.pack()
        self.graduation_year_entry = tk.Entry(self)
        self.graduation_year_entry.pack()

        self.submit_button = tk.Button(self, text="Export", command=self.export_eligible_students)
        self.submit_button.pack(pady=10)

    def export_eligible_students(self):
        graduation_year = self.graduation_year_entry.get()
        self.db.export_eligible_students(graduation_year)
        self.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()

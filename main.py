from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import csv

app = Flask(__name__)
app.secret_key = 'my secret key'

# Configure MySQL database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'placement_management_system'
}


def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('first.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (Username, Password, UserType) VALUES (%s, %s, %s)",
                       (username, password, 'user'))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE Username = %s AND Password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[0]
            session['user_type'] = user[2]
            return redirect(url_for('student'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')

    return render_template('login.html')
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM user WHERE Username = %s AND Password = %s", (username, password))
    #     result = cursor.fetchone()
    #     cursor.close()
    #     conn.close()
    #     if result:
    #         return "Login success"
    #     else:
    #         return "Invalid login"
    # return render_template('login.html')


@app.route('/student', methods=['GET'])
def student():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('student_table.html', students=students)


@app.route('/insert_student', methods=['GET', 'POST'])
def insert_student():
    if request.method == 'POST':
        usn = request.form['usn']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        department = request.form['department']
        graduation_year = request.form['graduation_year']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO student (USN, FirstName, LastName, ContactNumber, Email, Department, GraduationYear) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (usn, first_name, last_name, contact_number, email, department, graduation_year))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('student'))
    return render_template('insert_student.html')


@app.route('/insert_gpa', methods=['GET', 'POST'])
def insert_gpa():
    if request.method == 'POST':
        usn = request.form['usn']
        academic_year = request.form['academic_year']
        semester = request.form['semester']
        cumulative_gpa = request.form['cumulative_gpa']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO gpa (USN, AcademicYear, Semester, CumulativeGPA) VALUES (%s, %s, %s, %s)",
                       (usn, academic_year, semester, cumulative_gpa))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('student'))
    return render_template('insert_gpa.html')


@app.route('/company')
def company():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM company")
    companies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('company_table.html', companies=companies)

@app.route('/export_students/<int:year>', methods=['GET'])
def export_students(year):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE GraduationYear=%s", (year,))
    eligible_students = cursor.fetchall()
    with open(f'eligible_students_{year}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['USN', 'First Name', 'Last Name', 'Contact Number', 'Email', 'Department', 'Graduation Year'])
        writer.writerows(eligible_students)
    cursor.close()
    conn.close()
    return redirect(url_for('student'))


if __name__ == '__main__':
    app.run(debug=True)


#############################################################

# from flask import Flask, render_template
# import mysql.connector
#
# app = Flask(__name__)
#
# # Configure MySQL database
# db_config = {
#     'host': 'localhost',
#     'port': 8889,
#     'user': 'root',
#     'password': 'root',
#     'database': 'placement_management_system'
# }
#
# def get_db_connection():
#     conn = mysql.connector.connect(**db_config)
#     return conn
#
# @app.route('/')
# def index():
#     return render_template('first.html')
#
# @app.route('/company')
# def company():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM company")
#     companies = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template('company_table.html', companies=companies)
#
# @app.route('/student')
# def student():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM student")
#     students = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template('student_table.html', students=students)
#
# if __name__ == '__main__':
#     app.run(debug=True)
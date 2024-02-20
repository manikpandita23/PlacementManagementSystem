import mysql.connector

# Define database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'placement_management_system'
}

def create_database_and_tables():
    mysql_conn = None
    cursor = None
    try:
        # Connect to database
        mysql_conn = mysql.connector.connect(**db_config)
        cursor = mysql_conn.cursor()

        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS placement_management_system")

        # Connect to the newly created database
        mysql_conn.database = "placement_management_system"
        cursor = mysql_conn.cursor()

        # Create tables
        create_tables(cursor)

        # Commit changes (inside finally block)
        mysql_conn.commit()

    except mysql.connector.Error as err:
        print(f"Error creating database or tables: {err}")
    finally:
        # Close cursor and connection (separately)
        if cursor:
            cursor.close()
        if mysql_conn:
            mysql_conn.close()

def create_tables(cursor):
    # Define table creation statements (use separate statements for better clarity)
    create_company_table = """
    CREATE TABLE IF NOT EXISTS company (
        CompanyID INT PRIMARY KEY,
        CompanyName VARCHAR(255),
        Industry VARCHAR(255),
        Location VARCHAR(255),
        ContactPersonName VARCHAR(255),
        ContactEmail VARCHAR(255),
        Number VARCHAR(20)
    );
    """

    create_student_table = """
    CREATE TABLE IF NOT EXISTS student (
        USN VARCHAR(20) PRIMARY KEY,
        FirstName VARCHAR(255),
        LastName VARCHAR(255),
        ContactNumber VARCHAR(20),
        Email VARCHAR(255),
        Department VARCHAR(255),
        GraduationYear INT
    );
    """

    create_gpa_table = """
    CREATE TABLE IF NOT EXISTS gpa (
        USN VARCHAR(20),
        AcademicYear INT,
        Semester INT,
        CumulativeGPA FLOAT,
        PRIMARY KEY (USN, AcademicYear, Semester),
        FOREIGN KEY (USN) REFERENCES student(USN)
    );
    """

    create_job_table = """
    CREATE TABLE IF NOT EXISTS job (
        JobID INT PRIMARY KEY,
        CompanyID INT,
        JobTitle VARCHAR(255),
        Description TEXT,
        EligibleCGPA FLOAT,
        FOREIGN KEY (CompanyID) REFERENCES company(CompanyID)
    );
    """

    create_user_table = """
    CREATE TABLE IF NOT EXISTS user (
        Username VARCHAR(50) PRIMARY KEY,
        Password VARCHAR(255),
        UserType VARCHAR(50)
    );
    """

    # Execute table creation statements
    cursor.execute(create_company_table)
    cursor.execute(create_student_table)
    cursor.execute(create_gpa_table)
    cursor.execute(create_job_table)
    cursor.execute(create_user_table)

def insert_data(cursor):
    # Insert data into company table
    insert_company_data = """
    INSERT INTO company (CompanyID, CompanyName, Industry, Location, ContactPersonName, ContactEmail, Number) VALUES
    (1, 'ABC Corporation', 'Technology', 'New York', 'John Doe', 'john.doe@example.com', '123-456-7890'),
    (2, 'XYZ Enterprises', 'Finance', 'London', 'Jane Smith', 'jane.smith@example.com', '987-654-3210'),
    (3, 'PQR Ltd', 'Healthcare', 'Paris', 'Michael Johnson', 'michael.johnson@example.com', '456-789-0123'),
    (4, 'LMN Inc', 'Automobile', 'Tokyo', 'Emily Brown', 'emily.brown@example.com', '321-654-9870'),
    (5, 'EFG Group', 'Retail', 'Sydney', 'David Lee', 'david.lee@example.com', '789-012-3456');
    """
    cursor.execute(insert_company_data)

    # Insert data into student table
    insert_student_data = """
    INSERT INTO student (USN, FirstName, LastName, ContactNumber, Email, Department, GraduationYear) VALUES
    ('1CE17CS001', 'Alice', 'Johnson', '987-654-3210', 'alice.johnson@example.com', 'Computer Science', 2021),
    ('1CE17EC002', 'Bob', 'Williams', '123-456-7890', 'bob.williams@example.com', 'Electronics', 2022),
    ('1CE17ME003', 'Charlie', 'Brown', '456-789-0123', 'charlie.brown@example.com', 'Mechanical', 2023),
    ('1CE17IT004', 'David', 'Davis', '321-654-9870', 'david.davis@example.com', 'Information Technology', 2021),
    ('1CE17CV005', 'Emma', 'Miller', '789-012-3456', 'emma.miller@example.com', 'Civil', 2022);
    """
    cursor.execute(insert_student_data)

    # Insert data into gpa table
    insert_gpa_data = """
    INSERT INTO gpa (USN, AcademicYear, Semester, CumulativeGPA) VALUES
    ('1CE17CS001', 2020, 1, 3.5),
    ('1CE17CS001', 2020, 2, 3.6),
    ('1CE17CS001', 2021, 1, 3.7),
    ('1CE17EC002', 2020, 1, 3.2),
    ('1CE17EC002', 2020, 2, 3.4),
    ('1CE17EC002', 2021, 1, 3.6),
    ('1CE17ME003', 2020, 1, 3.0),
    ('1CE17ME003', 2020, 2, 3.1),
    ('1CE17ME003', 2021, 1, 3.3),
    ('1CE17IT004', 2020, 1, 3.7);
    """
    cursor.execute(insert_gpa_data)

    # Insert data into job table
    insert_job_data = """
    INSERT INTO job (JobID, CompanyID, JobTitle, Description, EligibleCGPA) VALUES
    (1, 1, 'Software Developer', 'Developing software applications.', 3.5),
    (2, 2, 'Financial Analyst', 'Analyzing financial data and trends.', 3.6),
    (3, 3, 'Medical Researcher', 'Conducting medical research studies.', 3.7),
    (4, 4, 'Automobile Engineer', 'Designing and developing automobile components.', 3.4),
    (5, 5, 'Retail Sales Associate', 'Assisting customers and managing inventory.', 3.0);
    """
    cursor.execute(insert_job_data)

    # Insert data into user table
    insert_user_data = """
    INSERT INTO user (Username, Password, UserType) VALUES
    ('john_doe', 'password123', 'admin'),
    ('jane_smith', 'abc@123', 'user'),
    ('michael_johnson', 'pass123', 'user'),
    ('emily_brown', 'password', 'admin'),
    ('david_lee', 'password456', 'user');
    """
    cursor.execute(insert_user_data)

def main():
    mysql_conn = None
    cursor = None
    try:
        # Connect to database
        mysql_conn = mysql.connector.connect(**db_config)
        cursor = mysql_conn.cursor()

        # Create database and tables
        create_database_and_tables()

        # Insert data into tables
        insert_data(cursor)

        # Commit changes
        mysql_conn.commit()

        print("Database setup completed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close cursor and connection (separately)
        if cursor:
            cursor.close()
        if mysql_conn:
            mysql_conn.close()

if __name__ == "__main__":
    main()

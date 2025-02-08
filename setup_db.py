import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Create Employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL,
    Salary INTEGER NOT NULL,
    Hire_Date TEXT NOT NULL
)
""")

# Insert employee data
employees_data = [
    (1, "Alice", "Sales", 50000, "2021-01-15"),
    (2, "Bob", "Engineering", 70000, "2020-06-10"),
    (3, "Charlie", "Marketing", 60000, "2022-03-20")
]

cursor.executemany("INSERT INTO Employees VALUES (?, ?, ?, ?, ?)", employees_data)

# Create Departments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Departments (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Manager TEXT NOT NULL
)
""")

# Insert department data
departments_data = [
    (1, "Sales", "Alice"),
    (2, "Engineering", "Bob"),
    (3, "Marketing", "Charlie")
]

cursor.executemany("INSERT INTO Departments VALUES (?, ?, ?)", departments_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup completed.")

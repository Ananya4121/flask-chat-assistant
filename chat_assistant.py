import sqlite3
import spacy
import re
from flask import Flask, request, jsonify

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def connect_db():
    return sqlite3.connect("company.db")

# Improved query processing using regex
def process_query(user_input):
    user_input = user_input.lower()

    # Show all employees in a department
    match = re.search(r"show me all employees in the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return f"SELECT * FROM Employees WHERE Department = '{department}'"

    # Manager query
    match = re.search(r"who is the manager of the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return f"SELECT Manager FROM Departments WHERE Name = '{department}'"

    # Employees hired after a date
    match = re.search(r"list all employees hired after (\d{4}-\d{2}-\d{2})", user_input)
    if match:
        date = match.group(1)
        return f"SELECT * FROM Employees WHERE Hire_Date > '{date}'"

    # Salary Expense
    match = re.search(r"what is the total salary expense for the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return f"SELECT SUM(Salary) FROM Employees WHERE Department = '{department}'"

    return None  # If no pattern matches

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("query")
    sql_query = process_query(user_input)

    if not sql_query:
        return jsonify({"response": "Sorry, I don't understand that query."})

    # Execute the SQL query
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()

    return jsonify({"response": results if results else "No results found."})

if __name__ == "__main__":
    app.run(debug=True)

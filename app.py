from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import re

app = Flask(__name__, template_folder="templates")  # Explicitly set template folder
CORS(app)  # Enable CORS for frontend requests

# Connect to SQLite database
def connect_db():
    return sqlite3.connect("company.db")

# Function to process user queries
def process_query(user_input):
    if not user_input:
        return None  # Return None if input is missing

    user_input = user_input.lower()

    # Show/List all employees in a department
    match = re.search(r"(?:show|list) all employees in the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return "SELECT Name FROM Employees WHERE Department = ?", (department,)

    # Manager query
    match = re.search(r"who is the manager of the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return "SELECT Manager FROM Departments WHERE Name = ?", (department,)

    # Employees hired after a date
    match = re.search(r"list all employees hired after (\d{4}-\d{2}-\d{2})", user_input)
    if match:
        date = match.group(1)
        return "SELECT Name FROM Employees WHERE Hire_Date > ?", (date,)

    # Employees hired before a date
    match = re.search(r"list all employees hired before (\d{4}-\d{2}-\d{2})", user_input)
    if match:
        date = match.group(1)
        return "SELECT Name FROM Employees WHERE Hire_Date < ?", (date,)

    # Total Salary Expense for a Department
    match = re.search(r"what is the total salary expense for the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return "SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,)

    # Find highest salary in a department
    match = re.search(r"who has the highest salary in the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return "SELECT Name, MAX(Salary) FROM Employees WHERE Department = ?", (department,)

    # Find lowest salary in a department
    match = re.search(r"who has the lowest salary in the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return "SELECT Name, MIN(Salary) FROM Employees WHERE Department = ?", (department,)

    # Count employees in a department
    match = re.search(r"how many employees are in the (\w+) department", user_input)
    if match:
        department = match.group(1).capitalize()
        return "SELECT COUNT(*) FROM Employees WHERE Department = ?", (department,)

    return None  # If no pattern matches

# API Route for Chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    # Debugging: Print received request data
    print("📥 Received request:", data)

    if not data or "query" not in data:
        return jsonify({"error": "Invalid request. Expected JSON with 'query' key."}), 400

    user_input = data.get("query")
    sql_query = process_query(user_input)

    if not sql_query:
        return jsonify({"response": "❌ Sorry, I don't understand that query."})

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(*sql_query)
    results = cursor.fetchall()
    conn.close()

    print("🔍 Generated SQL Query:", sql_query)  # Debugging
    print("✅ Query Results:", results)  # Debugging

    return jsonify({"response": results if results else "⚠ No results found."})

# Serve the Frontend
@app.route("/")
def home():
    return render_template("index.html")  # Load the frontend UI

if __name__ == "__main__":
    print("🚀 Available routes:", app.url_map)  # Debugging
    app.run(debug=True)

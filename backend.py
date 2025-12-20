from flask import Flask, request, jsonify
import csv, os, re
from datetime import datetime

app = Flask(__name__)

USERS_FILE = "users.csv"
EXPENSE_FILE = "expenses.csv"

# ---------- INITIALIZE CSV FILES ----------
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])

if not os.path.exists(EXPENSE_FILE):
    with open(EXPENSE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "date", "category", "amount", "note"])

# ---------- PASSWORD VALIDATION ----------
def valid_password(pwd):
    return (
        len(pwd) >= 6 and
        re.search("[A-Za-z]", pwd) and
        re.search("[0-9]", pwd) and
        re.search("[@#$!%*?&]", pwd)
    )

# ---------- SIGNUP ----------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data["username"]
    password = data["password"]

    with open(USERS_FILE, "r") as f:
        if username in f.read():
            return jsonify({"status": "error", "msg": "Username already exists"})

    if not valid_password(password):
        return jsonify({"status": "error", "msg": "Weak password"})

    with open(USERS_FILE, "a", newline="") as f:
        csv.writer(f).writerow([username, password])

    return jsonify({"status": "success"})

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    with open(USERS_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row == [data["username"], data["password"]]:
                return jsonify({"status": "success"})
    return jsonify({"status": "error"})

# ---------- ADD EXPENSE ----------
@app.route("/add_expense", methods=["POST"])
def add_expense():
    d = request.json
    with open(EXPENSE_FILE, "a", newline="") as f:
        csv.writer(f).writerow([
            d["username"],
            datetime.now().strftime("%Y-%m-%d"),
            d["category"],
            d["amount"],
            d["note"]
        ])
    return jsonify({"status": "saved"})

# ---------- SUMMARY ----------
@app.route("/summary/<username>")
def summary(username):
    daily = 0
    monthly = 0
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")

    with open(EXPENSE_FILE, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["username"] == username:
                if r["date"] == today:
                    daily += float(r["amount"])
                if r["date"].startswith(month):
                    monthly += float(r["amount"])

    return jsonify({"daily": daily, "monthly": monthly})

if __name__ == "__main__":
    app.run(debug=True)

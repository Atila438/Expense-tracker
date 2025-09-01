import argparse
import json
import os
import datetime

DATA_FILE = "expenses.json"

# ---------------- Helper Functions ----------------
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def generate_id(expenses):
    return max([exp["id"] for exp in expenses], default=0) + 1
# ---------------- Commands ----------------
def add_expense(description, amount, category, currency):
    expenses = load_expenses()
    expense = {
        "id": generate_id(expenses),
        "date": datetime.date.today().isoformat(),
        "description": description,
        "amount": amount,
        "category": category,
        "currency": currency.upper()  # Store in uppercase for consistency
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense['id']})")

def list_expenses():
    expenses = load_expenses()
    print("ID  Date       Description       Amount   Category   Currency")
    for exp in expenses:
        print(f"{exp['id']}   {exp['date']}  {exp['description']}  "
              f"{exp['amount']} {exp['currency']}   {exp['category']}")
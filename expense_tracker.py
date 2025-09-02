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

def delete_expense(expense_id):
    expenses = load_expenses()
    expenses = [exp for exp in expenses if exp["id"] != expense_id]
    save_expenses(expenses)
    print("Expense deleted successfully")

def summary(month=None):
    expenses = load_expenses()
    total = 0
    currency = "USD"
    for exp in expenses:
        exp_month = int(exp["date"].split("-")[1])
        if month is None or exp_month == month:
            total += exp["amount"]
            currency = exp["currency"]  # Assume same currency for summary
    if month:
        print(f"Total expenses for month {month}: {total} {currency}")
    else:
        print(f"Total expenses: {total} {currency}")

# ---------------- CLI Setup ----------------
def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

# Add expense
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", default="General")
    add_parser.add_argument("--currency", default="USD", help="Currency (e.g., USD, EUR, KES)")

# List expenses
    subparsers.add_parser("list")

 # Delete expense
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

# Summary
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", type=int, help="Month number (1-12)")

    args = parser.parse_args()

    # Run commands
    if args.command == "add":
        add_expense(args.description, args.amount, args.category, args.currency)
    elif args.command == "list":
        list_expenses()
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "summary":
        summary(args.month)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

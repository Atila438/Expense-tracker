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
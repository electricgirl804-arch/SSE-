import json
import os

DB_FILE = "database.json"
SUPPLIERS_FILE = "suppliers.json"
ORDERS_FILE = "orders.json"
USERS_FILE = "users.json"

DEFAULT_PRODUCTS = {
    "panels": [{"brand": "Jinko 550W", "watt": 550, "stock": 50, "price_SA": 450, "price_EG": 6000, "price_SD": 70000, "price_UAE": 450, "price_USD": 120, "serial": "SSE-PV550-001"}],
    "inverters": [{"brand": "Growatt 5KW", "kw": 5, "stock": 20, "price_SA": 2000, "price_EG": 25000, "price_SD": 300000, "price_UAE": 2000, "price_USD": 530, "serial": "SSE-INV5-001"}],
    "batteries": [{"brand": "Pylontech 100AH", "ah": 100, "stock": 25, "price_SA": 1800, "price_EG": 22000, "price_SD": 250000, "price_UAE": 1800, "price_USD": 480, "serial": "SSE-BAT100-001"}],
    "tax": {"SA": 0.15, "EG": 0.14, "SD": 0.17, "UAE": 0.05, "USD": 0.0},
    "shipping": {"SA": 200, "EG": 500, "SD": 10000, "UAE": 150, "USD": 50}
}

DEFAULT_SUPPLIERS = [{"brand": "كيبل تركي 6mm", "price": 2.0, "status": "مفعل"}]
DEFAULT_USERS = [{"email": "electricgirl804@gmail.com", "password": "shahd8499", "role": "admin"}]

def load_products():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(DEFAULT_PRODUCTS, f, ensure_ascii=False, indent=4)
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def load_suppliers():
    if not os.path.exists(SUPPLIERS_FILE):
        with open(SUPPLIERS_FILE, 'w', encoding='utf-8') as f: json.dump(DEFAULT_SUPPLIERS, f, ensure_ascii=False, indent=4)
    with open(SUPPLIERS_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def load_orders():
    if not os.path.exists(ORDERS_FILE): return []
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f: json.dump(DEFAULT_USERS, f, ensure_ascii=False, indent=4)
    with open(USERS_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_to_sheet(data, sheet_name):
    file = f"{sheet_name}.json"
    all_data = [] if not os.path.exists(file) else json.load(open(file, 'r', encoding='utf-8'))
    all_data.append(data)
    with open(file, 'w', encoding='utf-8') as f: json.dump(all_data, f, ensure_ascii=False, indent=4)
    return True

def save_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)
    return True

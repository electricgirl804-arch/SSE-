import json
import os

DB_FILE = "database.json"
SUPPLIERS_FILE = "suppliers.json"

# بيانات افتراضية لو الملف فاضي
DEFAULT_PRODUCTS = {
    "panels": [
        {"brand": "Jinko 550W", "watt": 550, "stock": 50, "price_SA": 450, "price_EG": 6000, "price_SD": 70000, "price_UAE": 450, "price_USD": 120, "serial": "SSE-PV550-001"},
        {"brand": "LONGi 545W", "watt": 545, "stock": 30, "price_SA": 430, "price_EG": 5800, "price_SD": 68000, "price_UAE": 430, "price_USD": 115, "serial": "SSE-PV545-002"}
    ],
    "inverters": [
        {"brand": "Growatt 5KW", "kw": 5, "stock": 20, "price_SA": 2000, "price_EG": 25000, "price_SD": 300000, "price_UAE": 2000, "price_USD": 530, "serial": "SSE-INV5-001"},
        {"brand": "Solis 10KW", "kw": 10, "stock": 15, "price_SA": 3500, "price_EG": 45000, "price_SD": 550000, "price_UAE": 3500, "price_USD": 930, "serial": "SSE-INV10-002"}
    ],
    "batteries": [
        {"brand": "Pylontech 100AH", "ah": 100, "stock": 25, "price_SA": 1800, "price_EG": 22000, "price_SD": 250000, "price_UAE": 1800, "price_USD": 480, "serial": "SSE-BAT100-001"}
    ],
    "tax": {"SA": 0.15, "EG": 0.14, "SD": 0.17, "UAE": 0.05, "USD": 0.0},
    "shipping": {"SA": 200, "EG": 500, "SD": 10000, "UAE": 150, "USD": 50}
}

DEFAULT_SUPPLIERS = [
    {"brand": "كيبل تركي 6mm", "price": 2.0, "status": "مفعل"},
    {"brand": "قاطع شنايدر", "price": 25, "status": "مفعل"}
]

def load_products():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f: json.dump(DEFAULT_PRODUCTS, f)
    with open(DB_FILE, 'r') as f: return json.load(f)

def load_suppliers():
    if not os.path.exists(SUPPLIERS_FILE):
        with open(SUPPLIERS_FILE, 'w') as f: json.dump(DEFAULT_SUPPLIERS, f)
    with open(SUPPLIERS_FILE, 'r') as f: return json.load(f)

def save_to_sheet(data, sheet_name):
    """بنحفظ في ملف محلي بدل قوقل شيت"""
    file = f"{sheet_name}.json"
    all_data = []
    if os.path.exists(file):
        with open(file, 'r') as f: all_data = json.load(f)
    all_data.append(data)
    with open(file, 'w') as f: json.dump(all_data, f)
    return True

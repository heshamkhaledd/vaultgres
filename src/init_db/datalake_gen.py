import json
import os
import random
import subprocess
import sys
import shutil
from faker import Faker
from collections import defaultdict

fake = Faker()

# Step 1: Get Git root
try:
    git_root = subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'],
        stderr=subprocess.STDOUT
    ).decode().strip()
except Exception as e:
    print("❌ Error retrieving Git top-level.\nDetails:", e)
    sys.exit(1)

# Step 2: Setup directories
data_root = os.path.join(git_root, "datalake")
users_dir = os.path.join(data_root, "users")
orders_dir = os.path.join(data_root, "orders")
inventory_dir = os.path.join(data_root, "inventory")

try:
    if os.path.exists(data_root):
        shutil.rmtree(data_root)
except Exception as e:
    print("❌ Error clearing existing data directory.\nDetails:", e)
    sys.exit(1)

os.makedirs(users_dir, exist_ok=True)
os.makedirs(orders_dir, exist_ok=True)
os.makedirs(inventory_dir, exist_ok=True)

# Step 3: Generate items (inventory/products)
product_names = list({fake.word().capitalize() for _ in range(30)})
inventory_catalog = {}
for i, name in enumerate(product_names, start=1):
    item = {
        "product_name": name,
        "available_quantity": random.randint(5, 20),
        "unit_price": round(random.uniform(10.0, 100.0), 2)
    }
    item_path = os.path.join(inventory_dir, f"item_{i}.json")
    with open(item_path, 'w') as f:
        json.dump(item, f, indent=4)
    inventory_catalog[name] = item

# Step 4: Generate users
users = []
for i in range(1, 21):
    user = {
        "id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip": fake.zipcode()
        },
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        "created_at": fake.iso8601()
    }
    with open(os.path.join(users_dir, f"user_{i}.json"), 'w') as f:
        json.dump(user, f, indent=4)
    users.append(user)

# Step 5: Generate orders referencing items (with stock validation)
order_index = 1
for user in users:
    num_orders = random.randint(1, 4)
    for _ in range(num_orders):
        selected_items = random.sample(list(inventory_catalog.keys()), k=random.randint(1, 3))
        order_items = []
        out_of_stock = False
        order_total = 0

        for name in selected_items:
            req_quantity = random.randint(1, 5)
            product = inventory_catalog[name]

            item_entry = {
                "product_name": name,
                "requested_quantity": req_quantity,
                "unit_price": product["unit_price"]
            }

            if req_quantity > product["available_quantity"]:
                out_of_stock = True
            else:
                order_total += req_quantity * product["unit_price"]

            order_items.append(item_entry)
            
        status_options = ['pending', 'transporting', 'delivered', 'cancelled']
        order = {
            "user_id": user["id"],
            "order_date": fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
            "status": "out of stock" if out_of_stock else random.choice(status_options),
            "total": 0 if out_of_stock else round(order_total, 2),
            "items": order_items
        }

        # Optionally decrement stock if fulfilled
        if not out_of_stock:
            for item in order_items:
                inventory_catalog[item["product_name"]]["available_quantity"] -= item["requested_quantity"]

        with open(os.path.join(orders_dir, f"order_{order_index}.json"), 'w') as f:
            json.dump(order, f, indent=4)

        order_index += 1

# Summary Log
print(f"Created {len(users)} users in: {users_dir}")
print(f"Created {len(product_names)} items in: {inventory_dir}")
print(f"Created {order_index - 1} orders in: {orders_dir}")

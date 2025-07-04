import json
import os
import sys
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from schema import *

class Client():
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def __del__(self):
        self.session.close()
        self.engine.dispose()

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    try:
        git_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            stderr=subprocess.STDOUT
        ).decode().strip()
        users_data_dir = os.path.join(git_root, 'datalake', 'users')
        order_items_data_dir = os.path.join(git_root, 'datalake', 'orders')
        inventory_data_dir = os.path.join(git_root, 'datalake', 'inventory')
    except Exception as e:
        print("❌ Error retrieving Git top-level.\nDetails:", e)
        sys.exit(1)

    db_config = load_json_data(os.path.join(git_root, 'src', 'init_db', 'db_config.json'))

    # postgresql+psycopg2://db_root:db_root@localhost:5432/vaultgres
    client = Client(f"postgresql+psycopg2://{db_config['db_admin_user']}:{db_config['db_admin_pass']}@{db_config['db_host']}:{db_config['db_port']}/{db_config['db_name']}")
    
    users_data = load_json_data(base_path / 'users.json')
    inventory_data = load_json_data(base_path / 'inventory.json')
    orders_data = load_json_data(base_path / 'orders.json')
    order_items_data = load_json_data(base_path / 'order_items.json')

    client.populate_users(users_data)
    client.populate_inventory(inventory_data)
    client.populate_orders(orders_data)
    client.populate_order_items(order_items_data)
    print("Database populated successfully.")
if __name__ == "__main__":
    main()
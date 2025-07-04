import json
import os
import sys
import subprocess
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class Datalake():
    def __init__(self, users_data_dir, orders_data_dir, inventory_data_dir):
        self.users_data_dir = users_data_dir
        self.orders_data_dir = orders_data_dir
        self.inventory_data_dir = inventory_data_dir

    @staticmethod
    def _load_json_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"File {file_path} not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Failed decoding JSON from {file_path}: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error reading {file_path}: {e}")
            sys.exit(1)

    def _nest_data_dicts(self, data_dir):
        data = {}
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                json_schema = filename.lower().split('.')[0]
                file_path = os.path.join(data_dir, filename)
                data[json_schema] = self._load_json_data(file_path)
        return data

    def get_users(self):
        return self._nest_data_dicts(self.users_data_dir)

    def get_inventory(self):
        return self._nest_data_dicts(self.inventory_data_dir)

    def get_orders(self):
        orders = self._nest_data_dicts(self.orders_data_dir)
        order_items = {}
        return orders, order_items

class Client():
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def __del__(self):
        self.session.close()
        self.engine.dispose()

    def populate_users(self, users_data):
        try:
            for user in users_data:
                new_user = User(**user)
                self.session.add(new_user)
            self.session.commit()
        except Exception as e:
            logger.error("Failed populating users:", e)
        finally:
            self.session.rollback()

    def populate_inventory(self, inventory_data):
        try:
            for item in inventory_data:
                new_item = Inventory(**item)
                self.session.add(new_item)
            self.session.commit()
        except Exception as e:
            logger.error("Failed populating inventory:", e)
        finally:
            self.session.rollback()

    def populate_orders(self, orders_data):
        try:
            for order in orders_data:
                new_order = Order(**order)
                self.session.add(new_order)
            self.session.commit()
        except Exception as e:
            logger.error("Failed populating orders:", e)
        finally:
            self.session.rollback()

    def populate_order_items(self, order_items_data):
        try:
            for item in order_items_data:
                new_item = OrderItem(**item)
                self.session.add(new_item)
            self.session.commit()
        except Exception as e:
            logger.error("Failed populating order items:", e)
        finally:
            self.session.rollback()

def valid_db_config(db_config):
    required_keys = ['db_admin_user', 'db_admin_pass', 'db_host', 'db_port', 'db_name']
    for key in required_keys:
        if key not in db_config:
            logger.error(f"Missing required database configuration key: {key}")
            return False
    return True

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
        logger.error("Failed retrieving Git top-level.\nDetails:", e)
        sys.exit(1)

    logger.info("Loading DB Configuration...")
    db_config = load_json_data(os.path.join(git_root, 'src', 'init_db', 'db_config.json'))
    
    if not valid_db_config(db_config):
        logger.error("Invalid database configuration. Please check db_config.json.\nExpecting keys: db_admin_user, db_admin_pass, db_host, db_port, db_name")
        sys.exit(1)
    
    # Preparing data for population
    logger.info("Loading data from Datalake...")
    datalake = Datalake(users_data_dir, order_items_data_dir, inventory_data_dir)
    users_data = datalake.get_users()
    inventory_data = datalake.get_inventory()
    [orders_data, order_items_data] = datalake.get_orders()

    # postgresql+psycopg2://db_root:db_root@localhost:5432/vaultgres
    logger.info("Populating Database...")
    client = Client(f"postgresql+psycopg2://{db_config['db_admin_user']}:{db_config['db_admin_pass']}@{db_config['db_host']}:{db_config['db_port']}/{db_config['db_name']}")
    client.populate_users(users_data)
    client.populate_inventory(inventory_data)
    client.populate_orders(orders_data)
    client.populate_order_items(order_items_data)
    logger.info("Database populated successfully.")

if __name__ == "__main__":
    main()
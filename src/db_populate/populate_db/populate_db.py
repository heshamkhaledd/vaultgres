import json
import os
import sys
import subprocess
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
import bcrypt
import traceback
from schema import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(message)s')
logger.handlers.clear()
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class Datalake():
    def __init__(self, users_data_dir, orders_data_dir, inventory_data_dir):
        self.users_data_dir = users_data_dir
        self.orders_data_dir = orders_data_dir
        self.inventory_data_dir = inventory_data_dir

    @staticmethod
    def _nest_data_dicts(data_dir):
        data = {}
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                json_schema = filename.lower().split('.')[0]
                file_path = os.path.join(data_dir, filename)
                data[json_schema] = load_json_data(file_path)
        return data

    def get_users(self):
        return self._nest_data_dicts(self.users_data_dir)

    def get_inventory(self):
        return self._nest_data_dicts(self.inventory_data_dir)

    def get_orders(self):
        order_map = {}
        orders = self._nest_data_dicts(self.orders_data_dir)
        for order in orders:
            order_items = orders[order].pop('items', {})
            order_map[order] = order_items
        return [orders, order_map]

class Client():
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def __del__(self):
        self.session.close()
        self.engine.dispose()

    @staticmethod
    def _dump_postgres_logs(self, message):
        with open('vaultgres.log', 'a') as log_file:
            log_file.write(f"{message}\n")

    @staticmethod
    def _hash_password(raw_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def populate_users(self, users_data):
        for user in users_data.values():
            user['password'] = self._hash_password(user['password'])
            new_user = User(**user)
            self.session.add(new_user)
            try:
                self.session.commit()
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    self._dump_postgres_logs(traceback.format_exc())
                else:
                    raise
            except Exception:
                logger.error(f"Unexpected error while committing user: {user}")
                self._dump_postgres_logs(traceback.format_exc())
            finally:
                self.session.rollback()

    def populate_inventory(self, inventory_data):
        for item in inventory_data.values():
            new_item = Inventory(**item)
            self.session.add(new_item)
            try:
                self.session.commit()
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    self._dump_postgres_logs(traceback.format_exc())
                else:
                    raise
            except Exception:
                logger.error(f"Unexpected error while committing item: {item}")
                self._dump_postgres_logs(traceback.format_exc())
            finally:
                self.session.rollback()

    def populate_orders(self, orders_data, order_items_data):
        for order in orders_data:
            new_order = Order(**orders_data[order])
            self.session.add(new_order)
            try:
                self.session.commit()
            except Exception:
                logger.error(f"Unexpected error while committing order: {order}")
                self._dump_postgres_logs(traceback.format_exc())
            finally:
                self.session.rollback()

            for item in order_items_data[order]:
                new_item = OrderItem(order_id=new_order.id, **item)
                self.session.add(new_item)
                try:
                    self.session.commit()
                except IntegrityError as e:
                    if isinstance(e.orig, UniqueViolation):
                        self._dump_postgres_logs(traceback.format_exc())
                    else:
                        raise
                except Exception:
                    logger.error(f"Unexpected error while committing order item: {item}")
                    self._dump_postgres_logs(traceback.format_exc())
                finally:
                    self.session.rollback()
            
def valid_db_config(db_config):
    required_keys = ['db_admin_user', 'db_admin_pass', 'db_host', 'db_port', 'db_name']
    for key in required_keys:
        if key not in db_config:
            logger.error(f"Missing required database configuration key: {key}")
            return False
    return True

def load_json_data(file_path):
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

def main():
    root = os.environ.get('PWD')
    users_data_dir = os.path.join(root, 'datalake', 'users')
    order_items_data_dir = os.path.join(root, 'datalake', 'orders')
    inventory_data_dir = os.path.join(root, 'datalake', 'inventory')

    logger.info("Loading DB Configuration...")
    db_config = load_json_data(os.path.join(root, 'db_config.json'))
    
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
    client.populate_orders(orders_data, order_items_data)
    logger.info("Database populated successfully.")

if __name__ == "__main__":
    main()
# Database Population (`db_populate`)

This module provides scripts and configuration for generating sample data and populating the Vaultgres PostgreSQL database. It supports both manual and Dockerized workflows.

## Directory Structure

- `populate_db/`
  - `datalake_gen.py`: Generates sample data (users, inventory, orders) in the datalake format.
  - `populate_db.py`: Loads data from the datalake into the database using SQLAlchemy ORM.
  - `schema.py`: Python ORM definitions for the database schema.
- `db_config.json`: Database connection settings.
- `db_wait.py`: Waits for the database to become available before running population scripts.
- `entry.sh`: Entrypoint for Docker: waits for DB, generates data, and populates the database.
- `requirements.txt`: Python dependencies for all scripts.

## Usage

### 1. Wait for Database (Optional, for automation)
To ensure the database is ready before running population scripts:
```bash
python3 db_wait.py
```
This script will block until the database is reachable using the settings in `db_config.json`.

### 2. Generate Sample Data
To create or refresh the datalake with random users, inventory, and orders:
```bash
python3 populate_db/datalake_gen.py
```

### 3. Populate the Database
To load all datalake data into the database (requires a running PostgreSQL instance and valid `db_config.json`):
```bash
python3 populate_db/populate_db.py
```
- Loads users, inventory, and orders from the datalake.
- Uses SQLAlchemy ORM models from `schema.py`.
- Logs actions and errors to `vaultgres.log` (if configured).

### 4. Schema Utilities
- Use `populate_db/schema.py` as a reference for the database structure or for schema validation/ORM mapping.

## Docker Workflow

When using Docker Compose, you do **not** need to run these scripts manually. The `entry.sh` script is executed automatically in the container.
The container waits for the database, generates the datalake, and populates the database automatically.

## Customization
- Edit `populate_db/datalake_gen.py` to change the structure or amount of generated data.
- Edit `populate_db/populate_db.py` to modify data loading logic or add new data sources.
- Update `db_config.json` for custom database connection settings.

---

**Tip:** These scripts run after initializing the database schema and before performing backups or maintenance.

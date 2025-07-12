# Database Initialization (`init_db`)

This directory contains all scripts and configuration files required to initialize the PostgreSQL database, set up the schema, and prepare the environment for use.

## Files
- `init_db.sh`: Main shell script to initialize the database, create users, and apply schema.
- `datalake_gen.py`: (Optional) Script to generate datalake.
- `db_config.json`: Configuration for database connection and credentials.
- `schema.sql`: SQL file defining all tables, relationships, and constraints.

## Usage

### 1. Initialize the Database
```bash
./init_db.sh
```
- Creates the database and applies the schema.
- Reads configuration from `db_config.json`.

### 2. Generate Datalake Data (Optional)
```bash
python3 datalake_gen.py
```
- Generates data for the datalake.

## Options
- Edit `db_config.json` to set database name, user, and password before running scripts.

---

*Run this step before populating or maintaining the database.*

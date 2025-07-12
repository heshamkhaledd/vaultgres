# Database Population (`populate_db`)

Scripts and utilities for populating the database with sample data and managing schema objects.

## Files
- `populate_db.py`: Main script to load data from the datalake into the database.
- `schema.py`: Python representation of the database schema (for validation or ORM).
- `vaultgres.log`: PostgreSQL log file for population operations.

## Usage

### 1. Populate the Database
```bash
python3 populate_db.py
```
- Loads users, inventory, and orders from the datalake.
- Logs actions to `vaultgres.log`.

### 2. Schema Utilities
- Use `schema.py` for schema validation or as a reference for ORM mapping.

## Options
- Edit `populate_db.py` to customize data loading or add new data sources.

---

*Run after initializing the database and before backup/maintenance.*

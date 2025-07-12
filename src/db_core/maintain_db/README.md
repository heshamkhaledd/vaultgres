# Database Maintenance (`maintain_db`)

Scripts for ongoing database administration: user management, backup, and recovery.

## Files
- `add_user.sh`: Add a new PostgreSQL user.
- `generate_recover_backup.sh`: Generate a backup and provide recovery instructions.
- `db_config.json`: Connection and credential configuration.

## Usage

### 1. Add a User
```bash
./add_user.sh --db_name <db_name> --username <user_name> --password <password> --access <admin|user>
```
- Creates a new user with secure defaults.

### 2. Generate Backup & Recovery
```bash
./generate_recover_backup.sh [--generate| --recover]
```
- Creates a backup of the database.
- Outputs instructions for restoring from backup.

## Options
- Edit `../db_config.json` to update connection details.

---

*Essential for production-like administration and disaster recovery.*

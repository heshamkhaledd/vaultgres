# Project Entrypoint

## `run.sh`

This is the main script to orchestrate the setup and management of your Vaultgres PostgreSQL environment.

## Usage
```bash
./run.sh
```

### Steps
- `init` : Initialize the database (calls `init_db/init_db.sh`)
- `populate` : Populate the database with sample data (calls `populate_db/populate_db.py`)
- `add-users (admin and read-only users)` : Add a new user (calls `maintain_db/add_user.sh`)
- `backup` : Generate a backup (calls `maintain_db/generate_recover_backup.sh --generate`)
- `recover` : Recovers DB using a backup (calls `maintain_db/generate_recover_backup.sh --backup`)
---

*Edit this script to customize orchestration or add new automation steps.*

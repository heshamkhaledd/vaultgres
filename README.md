# Vaultgres

**Vaultgres** is a hands-on PostgreSQL administration project for WSL (Ubuntu), simulating a production-ready database environment. It covers user management, security, backup, and recovery, ensuring data integrity and disaster recovery preparedness for real-world applications.

## Features
- Automated database initialization and schema setup
- User and access management scripts
- Data population and simulation
- Backup and recovery utilities
- Modular, organized codebase

## Directory Structure

- [`datalake/`](./datalake): Sample data for users, inventory, and orders (JSON format)
- [`src/init_db/`](./src/init_db): Database initialization scripts and schema
- [`src/maintain_db/`](./src/maintain_db): User management and backup scripts
- [`src/populate_db/`](./src/populate_db): Data population and schema utilities
- [`src/run.sh`](./src/run.sh): Main entrypoint for running the project

## Quick Start
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd vaultgres
   ```
2. **Run Everything (All in One)**
    ```bash
    cd src/
    ./run.sh
    ```
3. **Generate random datalake**
   ```bash
   cd init_db/
   python3 datalake_gen.py
   ```
4. **Initialize DB**
    ```bash
    ./init_db.sh [options]
    ```
4. **Populate with sample data**
   ```bash
   cd ../populate_db
   python3 populate_db.py
   ```
5. **Manage users and backups**
   ```bash
   cd ../maintain_db
   ./add_user.sh [options]
   ./generate_recover_backup.sh [options]
   ```

## Requirements
- WSL (Ubuntu)
- PostgreSQL
- Python 3.x

## Security & Recovery
- All scripts are designed with security and disaster recovery in mind.
- Backups are generated and can be restored easily.

---

Explore each directory for more details and usage instructions!

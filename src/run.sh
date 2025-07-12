# This script is used to run the entire project
#!/bin/bash

# Initalize the database with a db_root user
pushd init_db >/dev/null
./init_db.sh --clean
./init_db.sh
# Populate the database with initial data
popd >/dev/null
pushd populate_db >/dev/null
python3 datalake_gen.py
python3 populate_db.py
popd >/dev/null
# Create admin and user accounts
pushd maintain_db >/dev/null
./add_user.sh --db_name vaultgres --username admin --password admin --access admin
./add_user.sh --db_name vaultgres --username paravoid --password paravoid --access user
# Create a database backup for recovery (Can be later used in a crontab)
./generate_recover_backup.sh --generate
# Recover the database from the backup
./generate_recover_backup.sh --recover
popd >/dev/null

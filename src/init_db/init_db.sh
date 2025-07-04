#!/bin/bash
  
# Read database configuration from db_config.json file
if [ -f "db_config.json" ]; then
  echo "Reading database configuration from db_config.json..."
  DB_NAME=$(jq -r '.db_name' db_config.json)
  DB_ADMIN_USER=$(jq -r '.db_admin_user' db_config.json)
  DB_ADMIN_PASS=$(jq -r '.db_admin_pass' db_config.json)
else
  echo "Error: db_config.json file not found."
  exit 1
fi

# Clean up existing database and user
if [[ "$1" == "--clean" || "$1" == "--clear" || "$1" == "-c" ]]; then
  echo "Cleaning up existing database and user..."
  # Terminate active connections to vaultgres (except current session)
  sudo -u postgres psql -d postgres -c "
  SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE datname = '${DB_NAME}'
    AND pid <> pg_backend_pid();" > /dev/null

  # Drop database and user
  sudo -u postgres psql -d postgres -c "DROP DATABASE IF EXISTS ${DB_NAME};" > /dev/null
  sudo -u postgres psql -d postgres -c "DROP ROLE IF EXISTS ${DB_ADMIN_USER};" > /dev/null
  exit 0
fi

# Check if required variables are set
if [ -z "$DB_NAME" ] || [ -z "$DB_ADMIN_USER" ] || [ -z "$DB_ADMIN_PASS" ]; then
  echo "Error: Required database configuration variables are not set in db_config.json."
  exit 1
fi

# Check if admin user exists
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_ADMIN_USER}'" | grep -q 1; then
  echo "Creating database admin user..."
  sudo -u postgres psql -c "CREATE ROLE ${DB_ADMIN_USER} WITH LOGIN PASSWORD '${DB_ADMIN_PASS}';" > /dev/null
fi

# Check if database exists
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1; then
  echo "Creating database ${DB_NAME}..."
  sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_ADMIN_USER};" > /dev/null
fi

# Grant all privileges on the database to the admin user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_ADMIN_USER};" > /dev/null

# Execute schema using psql
if [ -f "schema.sql" ]; then
  SCHEMA_FILE="schema.sql"
else
  echo "Error: Schema file schema.sql not found."
  exit 1
fi
echo "Applying schema to the database..."
export PGPASSWORD="$DB_ADMIN_PASS"
psql -U "$DB_ADMIN_USER" -d "$DB_NAME" -h localhost -f "$SCHEMA_FILE" > /dev/null
unset PGPASSWORD
echo "Database and admin user setup completed successfully."
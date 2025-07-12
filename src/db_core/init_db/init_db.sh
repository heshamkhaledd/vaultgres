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

# Function to terminate active connections to a database
terminate_db_connections() {
    local db_name="$1"
    echo "Terminating active connections to ${db_name}..."
    sudo -u postgres psql -d postgres -c "
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = '${db_name}'
        AND pid <> pg_backend_pid();" >/dev/null
}

drop_database() {
    local db_name="$1"
    echo "Dropping database ${db_name}..."
    sudo -u postgres psql -d postgres -c "DROP DATABASE IF EXISTS ${db_name};" >/dev/null
}

drop_users() {
    # Find all login roles excluding postgres and the admin user
    ROLES_TO_DROP=$(
        sudo -u postgres psql -tAc "
        SELECT rolname FROM pg_roles
        WHERE rolcanlogin
        AND rolname NOT IN ('postgres', '${DB_ADMIN_USER}');"
    )

    # Reassign ownership and drop roles
    for ROLE in $ROLES_TO_DROP; do
        echo "Dropping user: $ROLE"
        sudo -u postgres psql -d postgres -c "REASSIGN OWNED BY ${ROLE} TO ${DB_ADMIN_USER};" >/dev/null
        sudo -u postgres psql -d postgres -c "DROP OWNED BY ${ROLE};" >/dev/null
        sudo -u postgres psql -d postgres -c "DROP ROLE IF EXISTS ${ROLE};" >/dev/null
    done
}

# Clean up existing database and user
if [[ "$1" == "--clean" || "$1" == "--clear" || "$1" == "-c" ]]; then
    echo "Cleaning up existing database and user..."
    terminate_db_connections "${DB_NAME}"
    drop_database "${DB_NAME}"

    # Drop the DB admin user
    sudo -u postgres psql -d postgres -c "DROP ROLE IF EXISTS ${DB_ADMIN_USER};" >/dev/null

    echo "Database and users cleaned."
    exit 0
elif [[ "$1" == "--recover" ]]; then
    echo "Dropping database, but keeping all users..."
    terminate_db_connections "${DB_NAME}"
    drop_database "${DB_NAME}"
fi

# Check if required variables are set
if [ -z "$DB_NAME" ] || [ -z "$DB_ADMIN_USER" ] || [ -z "$DB_ADMIN_PASS" ]; then
    echo "Error: Required database configuration variables are not set in db_config.json."
    exit 1
fi

# Check if admin user exists
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_ADMIN_USER}'" | grep -q 1; then
    echo "Creating database admin user..."
    sudo -u postgres psql -c "CREATE ROLE ${DB_ADMIN_USER} WITH LOGIN SUPERUSER PASSWORD '${DB_ADMIN_PASS}';" >/dev/null
fi

# Check if database exists
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1; then
    echo "Creating database ${DB_NAME}..."
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_ADMIN_USER};" >/dev/null
fi

if [ ! "$1" == "--recover" ]; then
    # Execute schema using psql
    if [ -f "schema.sql" ]; then
        SCHEMA_FILE="schema.sql"
    else
        echo "Error: Schema file schema.sql not found."
        exit 1
    fi
    echo "Applying schema to the database..."
    export PGPASSWORD="$DB_ADMIN_PASS"
    psql -U "$DB_ADMIN_USER" -d "$DB_NAME" -h localhost -f "$SCHEMA_FILE" >/dev/null
    unset PGPASSWORD
fi

echo "Database and admin user setup completed successfully."

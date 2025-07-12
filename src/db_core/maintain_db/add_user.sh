#!/bin/bash

#Create command-line arguments for database name, username, password, and access level (admin or user)
# Usage: ./add_user.sh --db_name <DB_NAME> --username <user_name> --password <password> --access <admin|user>
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

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
    --db_name)
        DB_NAME="$2"
        shift
        ;;
    --username)
        DB_USER="$2"
        shift
        ;;
    --password)
        DB_PASS="$2"
        shift
        ;;
    --access)
        ACCESS_LEVEL="$2"
        shift
        ;;
    *)
        echo "Unknown parameter passed: $1"
        exit 1
        ;;
    esac
    shift
done

# Check if required variables are set
if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ] || [ -z "$ACCESS_LEVEL" ]; then
    echo "Error: Required parameters are not set."
    echo "Usage: $0 --db_name <DB_NAME> --username <user_name> --password <password> --access <admin|user>"
    exit 1
fi

# Check if the access level is valid
if [[ "$ACCESS_LEVEL" != "admin" && "$ACCESS_LEVEL" != "user" ]]; then
    echo "Error: Invalid access level. Use 'admin' or 'user'."
    exit 1
fi

# Check if the database exists
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1; then
    echo "Error: Database '${DB_NAME}' does not exist."
    exit 1
fi

# Create the user with the specified password and access level
# Check if the user exists
USER_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'")

if [[ "$USER_EXISTS" != "1" ]]; then
    echo "User '${DB_USER}' does not exist. Creating..."
    sudo -u postgres psql -c "CREATE ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASS}';" >/dev/null
else
    echo "User '${DB_USER}' already exists. Updating password..."
    sudo -u postgres psql -c "ALTER ROLE ${DB_USER} WITH PASSWORD '${DB_PASS}';" >/dev/null
fi

# Grant CONNECT and SCHEMA USAGE in all cases
sudo -u postgres psql -d "$DB_NAME" -c "GRANT CONNECT ON DATABASE ${DB_NAME} TO ${DB_USER};" >/dev/null
sudo -u postgres psql -d "$DB_NAME" -c "GRANT USAGE ON SCHEMA public TO ${DB_USER};" >/dev/null

if [[ "$ACCESS_LEVEL" == "admin" ]]; then
    echo "Ensuring '${DB_USER}' has admin-level privileges on '${DB_NAME}'..."

    # Grant all privileges for tables, sequences, functions
    sudo -u postgres psql -d "$DB_NAME" <<EOF >/dev/null
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${DB_USER};
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${DB_USER};
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO ${DB_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO ${DB_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO ${DB_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO ${DB_USER};
EOF

else
    echo "Ensuring '${DB_USER}' has read-only privileges on '${DB_NAME}'..."

    # Only grant SELECT for tables
    sudo -u postgres psql -d "$DB_NAME" <<EOF >/dev/null
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO ${DB_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ${DB_USER};
EOF
fi
echo "User '${DB_USER}' created successfully with ${ACCESS_LEVEL} access to database '${DB_NAME}'."

# Print all users in the database
echo "Current users in database '${DB_NAME}':"
sudo -u postgres psql -d "$DB_NAME" -c "\du"

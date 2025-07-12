#!/bin/bash

# Configuration
if [ -f "db_config.json" ]; then
    echo "Reading database configuration from db_config.json..."
    DB_NAME=$(jq -r '.db_name' db_config.json)
    DB_ADMIN_USER=$(jq -r '.db_admin_user' db_config.json)
    DB_ADMIN_PASS=$(jq -r '.db_admin_pass' db_config.json)
    DB_HOST=$(jq -r '.db_host' db_config.json)
else
    echo "Error: db_config.json file not found."
    exit 1
fi
BACKUP_DIR="$HOME/db_backups/local"
DATE_SUFFIX=$(date +"%Y-%m-%d_%H-%M-%S")
FILENAME="${DB_NAME}_backup_${DATE_SUFFIX}.tar.gz"
ROTATION_LIMIT=7

# Parse command-line arguments
db_generate=0
db_recover=0
while [[ "$#" -gt 0 ]]; do
    case $1 in
    --generate)
        db_generate=1
        shift
        ;;
    --recover)
        db_recover=1
        shift
        ;;
    *)
        echo "Unknown parameter passed: $1"
        exit 1
        ;;
    esac
done

# Ensure flags are mutually exclusive
if [[ "$db_generate" -eq 1 && "$db_recover" -eq 1 ]]; then
    echo "Error: --generate and --recover flags cannot be used together"
    exit 1
fi

if [[ "$db_generate" -eq 0 && "$db_recover" -eq 0 ]]; then
    echo "Error: Either --generate or --recover flag must be specified"
    exit 1
fi

if [[ "$db_generate" -eq 1 ]]; then
    mkdir -p "$BACKUP_DIR"

    # Dump and compress the database
    echo "Generating backup for database '$DB_NAME'..."

    PGPASSWORD="$DB_ADMIN_PASS" pg_dump -U "$DB_ADMIN_USER" -h "$DB_HOST" -F t "$DB_NAME" >"$BACKUP_DIR/$FILENAME"

    if [[ $? -ne 0 ]]; then
        echo "Backup failed, Exiting..."
        exit 1
    fi

    echo "Backup saved to $BACKUP_DIR/$FILENAME"

    # Rotate old backups (keep latest ${ROTATION_LIMIT})
    echo "Rotating backups, keeping only the latest $ROTATION_LIMIT..."
    cd "$BACKUP_DIR"
    ls -1tr ${DB_NAME}_backup_*.tar.gz | head -n -"$ROTATION_LIMIT" | xargs -r rm --

elif [[ "$db_recover" -eq 1 ]]; then
    echo "Recovering database '$DB_NAME' from backup..."
    LATEST_BACKUP=$(ls -1t "$BACKUP_DIR"/${DB_NAME}_backup_*.tar.gz 2>/dev/null | head -n 1)
    if [[ -z "$LATEST_BACKUP" ]]; then
        echo "No backup found in $BACKUP_DIR"
        exit 1
    fi
    echo "Using latest backup: $LATEST_BACKUP"
    # Terminating all connections to the database before recovery
    echo "Terminating existing connections to $DB_NAME..."
    psql -d postgres -c "
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = '${DB_NAME}' AND pid <> pg_backend_pid();" > /dev/null
    if [[ $? -ne 0 ]]; then
        echo "Failed to terminate connections, Exiting..."
        exit 1
    fi
    # Drop and recreate the database
    echo "Dropping and recreating the database '$DB_NAME'..."
    ./init_db_docker.sh --recover
    if [[ $? -ne 0 ]]; then
        echo "Failed to drop and recreate the database, Exiting..."
        exit 1
    fi
    popd > /dev/null
    echo "Restoring backup into '$DB_NAME'..."
    PGPASSWORD=${DB_ADMIN_PASS} pg_restore -U "$DB_ADMIN_USER" -h "$DB_HOST" -d "$DB_NAME" -F t "$LATEST_BACKUP"

    if [[ $? -eq 0 ]]; then
        echo "Restore completed successfully."
    else
        echo "Restore failed."
        exit 1
    fi
fi

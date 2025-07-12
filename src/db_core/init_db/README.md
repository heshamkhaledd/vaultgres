# Database Initialization (`init_db`)

This directory contains all scripts and configuration files required to initialize the PostgreSQL database, set up the schema, and prepare the environment for use.

## Files
- `init_db.sh`: Main shell script to initialize the database, create root users, and apply schema.
- `schema.sql`: SQL file defining all tables, relationships, and constraints.

## Usage

### Dockerized Workflow
When using Docker Compose, database initialization is handled automatically by the entrypoint scripts in the relevant containers. You do not need to run `init_db.sh` manually unless you are customizing the process or running outside Docker.

## Options
- Edit `../db_config.json` to set database name, user, and password before running scripts.

---

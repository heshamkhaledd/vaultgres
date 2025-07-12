# Database Core (`db_core`)

This directory contains the core components for managing the PostgreSQL database in the Vaultgres project. It is organized into submodules for database initialization and ongoing maintenance.

## Files
- `db_config.json`: Configuration for database connection and credentials.

## Subdirectories
- `init_db/`: Scripts and configuration for initializing the database, setting up the schema, and preparing the environment. Includes tools for generating sample data.
- `maintain_db/`: Utilities for user management, backups, and other administrative tasks.

## Usage
These scripts are used as part of the automated Docker Compose setup. When running with Docker, the relevant scripts are executed automatically by the container entrypoints.

*Refer to the README files in each subdirectory for detailed instructions on initialization and maintenance tasks.*

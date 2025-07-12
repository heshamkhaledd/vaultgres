# Vaultgres

**Vaultgres** is a hands-on PostgreSQL administration project simulating a production-ready database environment. It covers user management, security, backup, and recovery, ensuring data integrity and disaster recovery preparedness for real-world applications.

## Features
- Automated database initialization and schema setup
- User and access management scripts
- Data population and simulation
- Backup and recovery utilities
- Modular, organized codebase
- Dockerized for easy setup and deployment

## Directory Structure
- db container
   - [`src/db_core/init_db/`](./src/db_core/init_db): Database initialization scripts and schema
   - [`src/db_core/maintain_db/`](./src/db_core/maintain_db): User management and backup scripts
- populator container
   - [`src/db_populate/`](./src/db_populate): Data population and schema utilities
- [`docker-compose.yml`](./docker-compose.yml): Multi-container orchestration for the project

## Quick Start (Docker)
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd vaultgres
   ```
2. **Start all services using Docker Compose**
   ```bash
   make up
   ```
   This will build and start the database and population services as defined in `docker-compose.yml`.

3. **Stop all services**
   ```bash
   make down
   ```
4. **Cleanup Build**
   ```bash
   make clean
   ```

## Requirements
- Linux Based OS (Using WSL Ubunutu)
- GNU Make (Using GNU Make 4.3)
- Docker Engine (Using Docker version 28.3.2, build 578ccf6)

---

Explore each directory for more details and usage instructions!

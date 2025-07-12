FROM postgres:15.1-alpine

# Install jq for parsing db_config.json
RUN apk add --no-cache jq

USER postgres

# --- Initialization setup ---
# Set working directory for init files
WORKDIR /docker-entrypoint-initdb.d/

# Copy init scripts and config
COPY --chown=postgres:postgres ./init_db/init_db_docker.sh .
COPY --chown=postgres:postgres ./init_db/db_config.json .
COPY --chown=postgres:postgres ./init_db/schema.sql .

# Ensure the init script is executable
RUN chmod +x init_db_docker.sh

# --- Maintenance scripts ---
WORKDIR /usr/src/vaultgres/maintain_db
COPY --chown=postgres:postgres ./maintain_db/add_user_docker.sh .
COPY --chown=postgres:postgres ./maintain_db/generate_recover_backup_docker.sh .

# Create symlinks to shared config/scripts
RUN ln -sfn /docker-entrypoint-initdb.d/db_config.json . && ln -sfn /docker-entrypoint-initdb.d/init_db_docker.sh .

# --- Project root ---
WORKDIR /usr/src/vaultgres
RUN ln -sfn /docker-entrypoint-initdb.d/ init_db

EXPOSE 5432

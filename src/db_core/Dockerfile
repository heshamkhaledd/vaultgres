FROM postgres:15.1-alpine

# Install jq for parsing db_config.json
RUN apk add --no-cache jq

USER postgres

# --- Initialization setup ---
# Set working directory for init files
WORKDIR /docker-entrypoint-initdb.d/

# Copy init scripts and config
COPY --chown=postgres:postgres ./init_db/* .
COPY --chown=postgres:postgres ./db_config.json .

# Ensure the init script is executable
RUN chmod +x init_db.sh

# --- Maintenance scripts ---
WORKDIR /usr/src/vaultgres/maintain_db
COPY --chown=postgres:postgres ./maintain_db/add_user.sh .
COPY --chown=postgres:postgres ./maintain_db/generate_recover_backup.sh .

# Create symlinks to shared config/scripts
RUN ln -sfn /docker-entrypoint-initdb.d/db_config.json . && ln -sfn /docker-entrypoint-initdb.d/init_db.sh .

# --- Project root ---
WORKDIR /usr/src/vaultgres
RUN ln -sfn /docker-entrypoint-initdb.d/ init_db

EXPOSE 5432

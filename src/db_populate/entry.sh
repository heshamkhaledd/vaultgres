#!/bin/bash

# Wait for the database to become reachable
if python3 db_wait.py; then
    python3 populate_db/datalake_gen.py
    python3 populate_db/populate_db.py
fi

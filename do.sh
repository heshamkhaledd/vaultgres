#!/bin/bash

if [[ "$1" == "--clean" || "$1" == "--clear" || "$1" == "-c" ]]; then
    docker compose down
    docker compose down --rmi all --volumes --remove-orphans
    exit 0
else
    docker compose up --build
fi

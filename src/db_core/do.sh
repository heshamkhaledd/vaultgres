#!/bin/bash

if [[ "$1" == "--clean" || "$1" == "--clear" || "$1" == "-c" ]]; then
    docker stop vaultgres
    docker rm vaultgres
    docker rmi vaultgres:0
    docker volume prune -f
    exit 0
else
    docker build -t vaultgres:0 .
    docker --debug run -d -e POSTGRES_PASSWORD=postgres -p 5432:5432 --name vaultgres vaultgres:0
    docker logs vaultgres
    docker exec -it vaultgres bash
fi

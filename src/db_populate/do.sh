#!/bin/bash

if [[ "$1" == "--clean" || "$1" == "--clear" || "$1" == "-c" ]]; then
    docker stop populate
    docker rm populate
    docker rmi populate:0
    docker volume prune -f
    exit 0
else
    docker build -t populate:0 .
    docker run -d --name populate populate:0
    sleep 2
    docker logs populate
    docker exec -it populate bash
fi

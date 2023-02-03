#!/bin/bash

docker build . -f docker_docs/Dockerfile_postgresql -t postgresql_docker
docker run --name database -d -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgresql_docker

docker build . -f docker_docs/Dockerfile_python -t python_docker
docker run --name app -d -p 5000:5000 --link database:postgresql python_docker


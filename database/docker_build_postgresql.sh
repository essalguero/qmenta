#!/bin/bash

docker build . -f Dockerfile_postgresql -t docker_postgresql
docker run --name database -d -v pgdata:/var/lib/postgresql/data -p 5432:5432 docker_postgresql


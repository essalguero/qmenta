#!/bin/bash

docker build . -f Dockerfile_python -t python_docker
docker run --name main -d -p 8000:8000 --link database:postgresql python_docker


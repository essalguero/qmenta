#!/bin/bash

docker build . -f Dockerfile -t docker_apache
docker run --name  docker_apache -d -p 8080:8080 docker_apache


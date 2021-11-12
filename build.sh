#!/bin/bash
echo "building web-server"
cd docker
bash build_docker.sh "$1"

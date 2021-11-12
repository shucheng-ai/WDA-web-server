#!/bin/bash

echo "$1"
rm -rf ../project/tmp
mkdir ../project/tmp
mkdir ../project/tmp/input
mkdir ../project/tmp/zip
rm ./config/cloud.py

if [ "$1" == "shell" ]
then
  echo "open shell:"
  server_path=$(cd "$(dirname "$0")";pwd)
  echo "/www/web-server"
  cd ..
  main_path=$(cd "$(dirname "$0")";pwd)
  docker run -it --rm -p 8008:8000 -v $main_path:/www -v /var/run/docker.sock:/var/run/docker.sock cyborg/webserver /bin/bash
elif [ "$1" == "dev" ]
then
  echo "run dev:"
  cd docker
  docker-compose -f docker-compose.dev.yml up
elif [ "$1" == "wsgi" ]
then
  echo "run wsgi server:"
  server_path=$(cd "$(dirname "$0")";pwd)
  cd ..
  main_path=$(cd "$(dirname "$0")";pwd)
  docker run -it --rm -p 8008:8000 -v $main_path:/www -v /var/run/docker.sock:/var/run/docker.sock cyborg/webserver sh -c 'cd /www/web-server && python3 start_server_v2_wsgi.py'
elif [ "$1" == "cloud" ]
then
  echo "run cloud:"
  cp cloud.py ./config/cloud.py
  cd docker
  docker-compose up -d
else
  echo "run server:"
  cd docker
  docker-compose up -d
fi



#!/bin/bash
# bash build_docker : 执行 cn 文件，编译镜像为换源版本
# bash build_docker en : 执行 en 文件，编译镜像不会执行换源操作
# bash build_docker.sh
# bash build_docker.sh en
# bash build_docker.sh ali
# bash build_docker.sh ustc
# bash build_docker.sh tsinghua

cp ../requirement.txt .
cp ../requirement.base.txt .
cp ../apt_install.sh .

if [ "$1" == "" ]
then
  echo "build cn(default ali) docker:"
  cp source/sources.ali.list sources.list
  cp source/pip.ali.conf pip.conf
  docker build -f Dockerfile.cn -t cyborg/webserver:3.0 . --no-cache
elif [ "$1" == "en" ]
then
  echo "build en docker:"
  docker build -f Dockerfile.en -t cyborg/webserver:3.0 . --no-cache
else
  echo "build cn($1) docker:"
  cp source/sources."$1".list sources.list
  cp source/pip."$1".conf pip.conf
  docker build -f Dockerfile.cn -t cyborg/webserver:3.0 . --no-cache
fi

docker tag cyborg/webserver:3.0 cyborg/webserver:latest
rm requirement.txt
rm requirement.base.txt
rm apt_install.sh 

echo "build docker ok!"

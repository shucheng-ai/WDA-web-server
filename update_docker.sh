cd docker 
docker build -f Dockerfile.update -t cyborg/webserver:update . --no-cache
docker tag cyborg/webserver:update cyborg/webserver:latest
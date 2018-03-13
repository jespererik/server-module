#server-module
The server module runs in a docker container.
To create the image run:

docker build -t server-module .

docker run -v ~/server-module/shared/:/server-module/shared/ --net=host -ti -d server-module:latest

To check log run:

tail -f shared/database.log
tailf -f shared/server.log

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)

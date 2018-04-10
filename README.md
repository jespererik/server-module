#server-module
The server module hosts a backend server and a frontend server.

From backend folder run:

docker build -t backend . 

From frontend folder run:

docker build -t frontend . 

From backend folder run and mount a shared volume for storage:

docker run -v $(pwd)/shared:/backend/shared --net=host -ti -d backend:latest

From frontend folder run:

docker run --net=host -ti -d frontend:latest

To check log run:

tail -f backend/shareddatabase.log
tailf -f backend/shared/server.log

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)

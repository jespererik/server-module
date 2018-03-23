#server-module
The server module hosts a backend server and a frontend server.

Run docker build -t backend . from backend folder

Run docker build -t frontend . from frontend folder
 
Run docker run -v $(pwd)/shared:/backend/shared --net=host -ti -d backend:latest from backend folder. This will mount a shared volume for storage.

Run docker run --net=host -ti -d frontend:latest from frontend folder

To check log run:

tail -f backend/shareddatabase.log
tailf -f backend/shared/server.log

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)

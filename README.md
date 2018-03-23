#server-module
The server module hosts a backend server and a frontend server.

Run docker build -t backend . from backend folder

Run docker build -t frontend . from frontend folder
 
Run docker run -v $(pwd)/backend/shared/:/backend/shared/ --net=host -ti -d backend:latest to start the backend and mount a shared volume for storage.

Run docker run --net-host -ti frontend:latest

To check log run:

tail -f backend/shareddatabase.log
tailf -f backend/shared/server.log

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)

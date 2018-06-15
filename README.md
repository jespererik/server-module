The server module hosts a backend server and a frontend server running in two Docker containers. 

When first running the applicaton use the build script which will build and start both the containers. 

Alternatively build and run the images with the commands below (it's important the the mount path is the same every time the container is started!): 

Navigate into backend folder and run:

docker build -t backend . 

Navigate intofrontend folder and run:

docker build -t frontend . 

From the backend folder run and mount a shared volume for storage:

docker run -v $(pwd)/shared:/backend/shared --net=host -ti -d --restart unless-stopped backend:latest

From the frontend folder run:

docker run --net=host -ti -d --restart unless-stopped frontend:latest

To check log:

tail -f backend/shareddatabase.log
tailf -f backend/shared/server.log

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)

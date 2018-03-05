FROM python:2

WORKDIR /server-module

ADD /shared ./shared
COPY /shared ./shared
ADD /sensorapp ./sensorapp

RUN pip install requests
RUN pip install flask

CMD ["python"]


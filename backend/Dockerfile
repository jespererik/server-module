FROM python:2

WORKDIR /backend

ADD . .

RUN pip install requests
RUN pip install flask
RUN pip install -U flask-cors

CMD python start.py


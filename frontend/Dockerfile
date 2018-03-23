FROM node:9.8.0

# Override the base log level (info).
ENV NPM_CONFIG_LOGLEVEL warn

WORKDIR /frontend

ADD . .

RUN npm run build --production

RUN npm install -g serve

CMD serve -s build

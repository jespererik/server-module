FROM node:stretch

# Override the base log level (info).
ENV NPM_CONFIG_LOGLEVEL warn

WORKDIR /frontend

ADD . .

ADD package.json package.json

RUN npm install --only=production

RUN npm run build --production

RUN npm install -g serve

CMD serve -s build

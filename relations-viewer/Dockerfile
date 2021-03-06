FROM node:15.11.0-alpine3.13

WORKDIR /app

COPY package.json .
COPY yarn.lock .
RUN yarn install --frozen-lockfile

COPY src/ src/
COPY public/ public/

ENTRYPOINT [ "yarn" ]
CMD [ "run", "start"]

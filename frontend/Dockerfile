FROM node:16-alpine3.13

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

ARG NEXT_PUBLIC_LOGIN_API_URL
ENV NEXT_PUBLIC_LOGIN_API_URL=${NEXT_PUBLIC_LOGIN_API_URL}

ARG NEXT_PUBLIC_ADOBE_API_KEY
ENV NEXT_PUBLIC_ADOBE_API_KEY=${NEXT_PUBLIC_ADOBE_API_KEY}

ARG PORT=3000
ENV PORT $PORT
EXPOSE $PORT

# you'll likely want the latest npm, regardless of node version, for speed and fixes
# but pin this version for the best stability
RUN npm i npm@latest -g

# install dependencies first, in a different location for easier app bind mounting for local development
# due to default /opt permissions we have to create the dir with root and change perms
RUN mkdir -p /opt/node_app/app && chown node:node -R /opt/node_app
WORKDIR /opt/node_app/app
# the official node image provides an unprivileged user as a security best practice
# but we have to manually enable it. We put it here so npm installs dependencies as the same
# user who runs the app.
# https://github.com/nodejs/docker-node/blob/master/docs/BestPractices.md#non-root-user
#USER node
COPY --chown=node:node package.json package-lock.json* ./
RUN npm install && npm cache clean --force && mv node_modules ../ && mkdir node_modules && chown node:node node_modules
ENV PATH /opt/node_app/node_modules/.bin:$PATH

COPY --chown=node:node . .

RUN npm run build

CMD [ "npm", "run", "start" ]
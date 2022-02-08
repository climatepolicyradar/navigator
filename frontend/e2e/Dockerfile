FROM cypress/included:9.4.1

WORKDIR /opt
RUN npm install cypress-file-upload
WORKDIR /opt/e2e

RUN npx cypress verify

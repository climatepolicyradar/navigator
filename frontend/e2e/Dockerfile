FROM cypress/included:9.4.1

WORKDIR /opt
RUN npm install cypress-file-upload cypress-pseudo-localization dotenv
WORKDIR /opt/e2e

RUN npx cypress verify

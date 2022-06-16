FROM cypress/included:10.1.0

# TODO: setup a proper unprivileged test user for cypress
ARG LOGIN_NAME: ${LOGIN_NAME}
ENV LOGIN_NAME=${LOGIN_NAME}

ARG LOGIN_PW: ${LOGIN_PW}
ENV LOGIN_PW=${LOGIN_PW}

WORKDIR /opt
RUN npm install cypress-file-upload cypress-pseudo-localization dotenv
WORKDIR /opt/e2e

RUN npx cypress verify

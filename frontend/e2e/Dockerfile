FROM cypress/included:9.4.1

WORKDIR /e2e

COPY package.json .
COPY package-lock.json .

RUN npm ci
RUN npx cypress verify

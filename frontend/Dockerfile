FROM node:16-alpine3.13

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build

EXPOSE 8000

CMD [ "npm", "run", "start" ]
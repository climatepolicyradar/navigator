FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y cmake

RUN mkdir ~/.ssh
RUN ssh-keyscan -H github.com >> ~/.ssh/known_hosts
RUN git clone https://github.com/kermitt2/pdfalto.git
RUN --mount=type=ssh cd pdfalto && git submodule update --init --recursive
RUN cd pdfalto && cmake .
RUN cd pdfalto && make

# Copy files to image
COPY . .

ENV PDFALTO_PATH=/app/pdfalto/pdfalto

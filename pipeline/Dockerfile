FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y cmake

RUN mkdir ~/.ssh
RUN ssh-keyscan -H github.com >> ~/.ssh/known_hosts
RUN git clone https://github.com/kermitt2/pdfalto.git
# Set submodule URL to HTTPS to avoid need for SSH setup when run on a server
RUN cd pdfalto && git submodule set-url xpdf-4.03 https://github.com/kermitt2/xpdf-4.03.git && git submodule update --init --recursive
RUN cd pdfalto && cmake .
RUN cd pdfalto && make

RUN pip install --upgrade pip
RUN pip install "poetry==1.1.8"


# Copy files to image
COPY . .

# Install python dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENV PDFALTO_PATH=/app/pdfalto/pdfalto

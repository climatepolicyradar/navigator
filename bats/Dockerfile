FROM bats/bats:latest 
RUN apk add git
RUN mkdir /opt/bats-test-helpers 
RUN cd /opt/bats-test-helpers 
RUN git clone https://github.com/ztombol/bats-support ./bats-support
RUN git clone https://github.com/ztombol/bats-assert ./bats-assert
RUN git clone https://github.com/lox/bats-mock ./lox-bats-mock
WORKDIR /code/

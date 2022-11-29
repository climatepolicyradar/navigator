FROM bats/bats:latest
RUN apk add git
RUN mkdir /opt/bats-test-helpers
RUN git clone https://github.com/ztombol/bats-support /opt/bats-test-helpers/bats-support
RUN git clone https://github.com/ztombol/bats-assert /opt/bats-test-helpers/bats-assert
RUN git clone https://github.com/lox/bats-mock /opt/bats-test-helpers/lox-bats-mock
WORKDIR /code/

FROM python:3.7

RUN apt-get update \
     apt-get install -y git

RUN mkdir opencard_test

WORKDIR ./opencard_test
#WORKDIR "/opencard_test"

#ADD https://github.com/600comp/opencard_test.git -b simlpe_test --depth=1

ARG username
ARG password

RUN git clone https://${username}:${password}@github.com/600comp/opencard_test.git  -b simlpe_test --depth=1

#COPY . .

RUN pip install -r requirements.txt

WORKDIR /

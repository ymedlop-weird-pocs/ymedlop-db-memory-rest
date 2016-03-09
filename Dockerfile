FROM ubuntu:latest

MAINTAINER BBVA Google Cloud Platform Team  <gcp.team@bbva.com>

RUN apt-get update

RUN apt-get install -y \
    python-dev python-pip \
    libspatialite-dev spatialite-bin

RUN apt-get clean all

ADD requirements.txt /tmp/requirements.txt
RUN pip install  -U -r /tmp/requirements.txt

ADD rest /tmp/rest
WORKDIR /tmp/rest

EXPOSE 5000

CMD ["python", "main.py"]
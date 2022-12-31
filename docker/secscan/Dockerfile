FROM python:3.10.9-bullseye
MAINTAINER Jonas.Winkler

COPY ./secscan /secscan

WORKDIR /secscan

RUN pip install -r requirements/base.txt

COPY ./docker/secscan/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN set -x \
    && apt-get update -y \

ENTRYPOINT ["/entrypoint.sh"]
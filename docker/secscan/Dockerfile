FROM python:3.10.9-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./secScan /app
COPY ./docker/secscan/entrypoint.sh /entrypoint.sh

RUN set -ex \
    && apt-get update

RUN pip install -r /app/requirements/requirements-pip.txt

WORKDIR /app

EXPOSE 8010

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
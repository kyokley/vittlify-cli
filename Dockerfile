FROM python:2.7-alpine

RUN apk add --no-cache \
            gcc \
            libffi-dev \
            openssl-dev \
            musl-dev

COPY . /app
WORKDIR /app
RUN pip install .

ENTRYPOINT ["vt"]

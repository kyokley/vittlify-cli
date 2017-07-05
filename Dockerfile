FROM python:2.7-alpine

RUN apk add --no-cache \
            gcc \
            libffi-dev \
            openssl-dev \
            musl-dev

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app
RUN pip install .

ENTRYPOINT ["vt"]

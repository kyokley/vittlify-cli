ARG BASE_IMAGE=python:3.8-alpine

FROM ${BASE_IMAGE} AS base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
RUN apk add --no-cache libffi-dev openssl-dev musl-dev

FROM base AS builder
RUN apk add --no-cache gcc \
                       git

RUN pip install --upgrade pip wheel setuptools poetry \
    git+https://github.com/kyokley/terminaltables.git

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

RUN poetry install --no-dev

FROM builder AS dev-builder
RUN poetry install

FROM base AS prod

COPY --from=builder /venv /venv
COPY . /app

ENTRYPOINT ["poetry", "run", "vt"]

FROM base AS dev
COPY --from=dev-builder /venv /venv

COPY . /app
ENTRYPOINT ["poetry", "run", "vt"]

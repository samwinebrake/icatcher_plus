# test dockerfile.. testing automated build
FROM python:3.9

RUN mkdir /src

COPY /src /src
COPY pyproject.toml /src 

WORKDIR /src
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

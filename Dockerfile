# test dockerfile.. testing automated build
FROM python:3.9

RUN mkdir /src
RUN mkdir /src/icatcher

COPY /src/icatcher /src/icatcher
COPY pyproject.toml /src/icatcher

WORKDIR /src/icatcher
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN python -m pip install .
# RUN pip3 install poetry
# RUN poetry config virtualenvs.create false
# RUN poetry install --no-dev

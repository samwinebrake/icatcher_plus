# test dockerfile.. testing automated build
# FROM python:3.9

# get permission denied with this
FROM  xychelsea/ffmpeg-nvidia:latest-jupyter

RUN conda install anaconda-client -n base

RUN conda update conda
RUN conda config --append channels pytorch
RUN conda config --append channels anaconda
RUN conda config --append channels conda-forge
RUN conda config --append channels defaults

RUN conda install python=3.9
RUN conda install pip
RUN conda install -c conda-forge ffmpeg
RUN conda install pytorch
RUN pip install icatcher

ENV ICATCHER_DATA_DIR=/models
RUN mkdir /models

# RUN mkdir /src
# RUN mkdir /src/icatcher

# COPY /src/icatcher /src/icatcher
# COPY pyproject.toml /src/icatcher

# WORKDIR /src/icatcher
# ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# RUN python -m pip install --upgrade pip
# RUN python -m pip install .
# # RUN pip3 install poetry
# # RUN poetry config virtualenvs.create false
# # RUN poetry install --no-dev



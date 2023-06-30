FROM  xychelsea/ffmpeg-nvidia:latest-jupyter

RUN conda install anaconda-client -n base
RUN conda update conda


RUN conda install python=3.9
RUN conda install pip
RUN conda install -c conda-forge ffmpeg
RUN pip install icatcher

# change user to root so can mkdir
USER root

RUN mkdir /models
ENV ICATCHER_DATA_DIR=/models

USER ${ANACONDA_UID}


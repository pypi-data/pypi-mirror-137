FROM debian:latest
RUN apt-get update && \
    apt-get install -y \
      pylint3 python3-pip tox git \
      curl pycodestyle \
      python3-sphinx
ARG COMMIT="dev"
RUN git clone -b dev https://gitlab.indiscale.com/caosdb/src/caosdb-pylib.git && \
    cd caosdb-pylib && git checkout $COMMIT && pip3 install .
RUN pip3 install recommonmark sphinx-rtd-theme

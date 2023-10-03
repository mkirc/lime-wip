FROM ubuntu:latest

RUN apt-get update \
        && apt-get install -y \
            build-essential \
            libgsl-dev \
            libcfitsio-dev \
            libatlas-base-dev \
            libncurses-dev \
            libqhull-dev \
            libqhull8.0 \
            gcc \
            libhdf5-dev \
            python3 \
            python-dev-is-python3 \
        && mkdir /lime /lime-tools /model

COPY configure /lime-tools
COPY lime-run /lime-tools

ENV PATH=/lime-tools:/lime:${PATH}

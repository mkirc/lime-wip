#!/usr/bin/env bash

docker run -it -v ./../lime:/lime -v ./models/hdf5:/model lime-dev lime-run --hdf5 --no-ncurses ./model.c

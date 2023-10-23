#!/usr/bin/env bash

docker run -it -v ./lime-1.9.5.hdf5~patch:/lime -v ./models/inFileTest:/model lime-dev lime-run

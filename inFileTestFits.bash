#!/usr/bin/env bash

docker run -it -v ./lime-1.9.5:/lime -v ./models/inFileTestFits:/model lime-dev lime-run

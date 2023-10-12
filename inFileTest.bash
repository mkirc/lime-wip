#!/usr/bin/env bash

docker run -it -v ./lime-1.9.5:/lime -v ./models/inFileTest:/model lime-dev lime-run

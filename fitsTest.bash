#!/usr/bin/env bash

docker run -it -v ./../lime:/lime -v ./models/fits:/model lime-dev lime-run

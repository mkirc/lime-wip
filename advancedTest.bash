#!/usr/bin/env bash

docker run -it -v ./../lime:/lime -v ./models/advanced:/model lime-dev lime-run


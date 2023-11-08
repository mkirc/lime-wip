#!/usr/bin/env bash

docker run -it -v ./../lime:/lime -v ./models/outFilesTestFits:/model lime-dev lime-run

#!/bin/bash

PIPELINE_NAME=$2
if [ "$1" == "upload-version" ]; then
    PIPELINE_VERSION=$3
    PIPELINE_PATH=$4
    kfp pipeline upload-version \
        -n "$PIPELINE_NAME" \
        -v $PIPELINE_VERSION \
        $PIPELINE_PATH
elif [ "$1" == "upload-new" ]; then
    PIPELINE_PATH=$3
    kfp pipeline upload \
        -p "$PIPELINE_NAME" \
        $PIPELINE_PATH
fi
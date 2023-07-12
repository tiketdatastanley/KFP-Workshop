#!/bin/bash

if [ "$1" == "gen_data" ]; then
    python -m src.pipelines.gen_data
elif [ "$1" == "retrain" ]; then
    python -m src.pipelines.retrain
elif [ "$1" == "train" ]; then
    python -m src.pipelines.train
elif [ "$1" == "all" ]; then
    python -m src.pipelines.gen_data
    python -m src.pipelines.retrain
    python -m src.pipelines.train    
else
    echo "Invalid command option."
fi
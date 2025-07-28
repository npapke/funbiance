#!/bin/bash

cd $(dirname $0)
conda run -n py312 python -m funbiance


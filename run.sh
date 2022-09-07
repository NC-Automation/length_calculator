#!/bin/bash

RELATIVEDIR=`echo $0|sed s/run.sh//g`
cd $RELATIVEDIR

chmod +x ./src/length_calc.py
python3 -u ./src/length_calc.py

#!/bin/bash

virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt

while [ 1 ]
do
  youtube/youtube.py
  sleep 1
  clear
  read -n 1 -t 0.1 input
    if [[ $input = "q" ]] || [[ $input = "Q" ]]
    then
        exit
    fi
done

#!/bin/bash
docker pull mongo
docker run -p 27017:27017 --name mongo3 mongo:jessie

python database/mongo_insert.py

. $HOME/workspace/monsters/config/export_env.sh

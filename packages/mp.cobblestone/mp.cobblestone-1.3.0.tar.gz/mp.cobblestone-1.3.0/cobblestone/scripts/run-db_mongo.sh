#!/bin/sh

# -----------------------------------------------------------------------
# Copyright 2022 Mina Pêcheux

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at the root of the repo.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------

DB_PORT=${DB_PORT:-27017}

display_usage() {
  echo ""
  echo "usage :"
  echo "$0 [--port PORT]"
  echo ""
  echo "--port: specific port to run the DB on (default: 27017)"
  echo ""
}

for key in "$@"
do

case $key in
  --help|-h)
  echo help
  display_usage
  exit 0
  shift
  ;;
  --port)
  DB_PORT="$2"
  shift
  ;;
  *)    # unknown option
  shift
  ;;
esac
done

# Create network if need be
NETWORK_NAME=cobblestone
if [ ! "$(docker network ls | grep -w ${NETWORK_NAME})" ]; then
  echo "Creating network: ${NETWORK_NAME}!"
  docker network create ${NETWORK_NAME}
else
  echo "${NETWORK_NAME} network already exists!"
fi

# Pull Mongo image if need be
docker pull mvertes/alpine-mongo

# Run Mongo image
DB_CONTAINER_NAME=cobblestone-database
if [ "$(docker ps -aq -f name=${DB_CONTAINER_NAME})" ]; then
  docker rm -f $(docker ps -aq -f name=${DB_CONTAINER_NAME})
fi

docker run -d \
  --name ${DB_CONTAINER_NAME} \
  --net ${NETWORK_NAME} \
  -p 127.0.0.1:${DB_PORT}:27017 \
  -v $(pwd)/db:/data/db \
  mvertes/alpine-mongo

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

DB_WEB_PORT=${DB_WEB_PORT:-7474}
DB_BOLT_PORT=${DB_PORT:-7687}

display_usage() {
  echo ""
  echo "usage :"
  echo "$0 [--web-port PORT] [--bolt-port PORT]"
  echo ""
  echo "--web-port: specific port to run the DB webserver on (default: 7474)"
  echo "--bolt-port: specific port to run the DB bolt on (default: 7687)"
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
  --web-port)
  DB_WEB_PORT="$2"
  shift
  ;;
  --bolt-port)
  DB_BOLT_PORT="$2"
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

# Pull Neo4j image if need be
docker pull neo4j:3.5.8

# Run Neo4j image
DB_CONTAINER_NAME=cobblestone-database
if [ "$(docker ps -aq -f name=${DB_CONTAINER_NAME})" ]; then
  docker rm -f $(docker ps -aq -f name=${DB_CONTAINER_NAME})
fi

docker run -d \
  --name ${DB_CONTAINER_NAME} \
  --net ${NETWORK_NAME} \
  -p ${DB_WEB_PORT}:7474 -p ${DB_BOLT_PORT}:7687 \
  -v $(pwd)/db/main/data/:/data \
  -v $(pwd)/db/main/logs/:/logs \
  -v $(pwd)/db/main/plugins/:/plugins \
  neo4j:3.5.8 /sbin/tini -g -- /docker-entrypoint.sh neo4j

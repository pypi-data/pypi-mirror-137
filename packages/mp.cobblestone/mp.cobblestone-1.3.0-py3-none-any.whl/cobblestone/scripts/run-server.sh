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

DEBUG=0

display_usage() {
  echo ""
  echo "usage :"
  echo "$0 [--debug]"
  echo ""
  echo "--debug: if true, run in debug mode with hot reload"
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
  --debug)
  DEBUG=1
  shift
  ;;
  *)    # unknown option
  shift
  ;;
esac
done

if [ ${DEBUG} -eq 1 ]; then
  uvicorn cobblestone.server:app --host ${API_HOST} --port ${API_PORT} --reload
else
  uvicorn cobblestone.server:app --host ${API_HOST} --port ${API_PORT}
fi

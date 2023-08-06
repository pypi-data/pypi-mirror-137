FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

RUN mkdir -p /usr/src/app/cobblestone

# install base dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

# copy FastAPI app, database init script and environment file
COPY ./.env /usr/src/app/.env
COPY ./db_init.py /usr/src/app/db_init.py
COPY ./cobblestone /usr/src/app/cobblestone

# finalize settings
ENV MODULE_NAME cobblestone.server

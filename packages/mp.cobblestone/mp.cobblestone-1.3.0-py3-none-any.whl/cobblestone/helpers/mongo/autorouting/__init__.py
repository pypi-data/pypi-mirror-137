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

import importlib
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional

from cobblestone.helpers.utils import inflector
from cobblestone.security import oauth2_scheme
from cobblestone.tokens import check_token


from .create import create_instance_handler
from .read import list_instances_handler, get_instance_by_uid_handler, OrderingDirections
from .update import patch_at_uid_handler
from .delete import delete_all_instances_handler, delete_instance_by_uid_handler


HANDLERS = {}


def create_handlers(schema: str, raw_name: str):
    schemas_module = importlib.import_module(
        '.' + raw_name, 'cobblestone.models')
    full_schema = getattr(schemas_module, schema + 'Full')
    db_schema = getattr(schemas_module, schema + 'InDB')

    HANDLERS[f'{schema}__create_instance_handler'] = \
        create_instance_handler(schema, db_schema, full_schema)
    HANDLERS[f'{schema}__list_instances_handler'] = \
        list_instances_handler(db_schema)
    HANDLERS[f'{schema}__get_instance_by_uid_handler'] = \
        get_instance_by_uid_handler(db_schema)
    HANDLERS[f'{schema}__patch_at_uid_handler'] = \
        patch_at_uid_handler(db_schema)
    HANDLERS[f'{schema}__delete_all_instances_handler'] = \
        delete_all_instances_handler(db_schema)
    HANDLERS[f'{schema}__delete_instance_by_uid_handler'] = \
        delete_instance_by_uid_handler(db_schema)


def create_router(app: FastAPI, schema: str, raw_name: str):
    schemas_module = importlib.import_module(
        '.' + raw_name, 'cobblestone.models')
    base_schema = getattr(schemas_module, schema)
    payload_schema = getattr(schemas_module, schema + 'Payload', base_schema)
    return_schema = getattr(schemas_module, schema + 'InDB').response_model

    # (some special cases are handled by hand)
    if raw_name == 'notes':
        raw_name_plural = 'notes'
    else:
        raw_name_plural = inflector.plural(raw_name)

    # CREATE ==========================
    @app.post(
        '/{}'.format(raw_name_plural),
        response_model=return_schema,
        tags=[raw_name_plural],
        status_code=201,
    )
    async def create_instance(instance_data: payload_schema, token: str = Depends(oauth2_scheme)) -> dict:
        check_token(token)
        return HANDLERS[f'{schema}__create_instance_handler'](instance_data)

    # READ ===========================
    @app.get(
        '/{}'.format(raw_name_plural),
        response_model=List[return_schema],
        tags=[raw_name_plural],
    )
    async def list_instances(
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        sort_dir: OrderingDirections = 'asc',
        token: str = Depends(oauth2_scheme)
    ) -> List[Dict]:
        check_token(token)
        return HANDLERS[f'{schema}__list_instances_handler'](skip, limit, sort_by, sort_dir)

    @app.get(
        '/{}/{{uid}}'.format(raw_name_plural),
        response_model=return_schema,
        tags=[raw_name_plural],
    )
    def get_instance_by_uid(uid: str, token: str = Depends(oauth2_scheme)) -> dict:
        check_token(token)
        return HANDLERS[f'{schema}__get_instance_by_uid_handler'](uid)

    # UPDATE =========================
    @app.patch(
        '/{}/{{uid}}'.format(raw_name_plural),
        response_model=return_schema,
        tags=[raw_name_plural],
    )
    def patch_at_uid(uid: str, update: dict, token: str = Depends(oauth2_scheme)) -> dict:
        check_token(token)
        return HANDLERS[f'{schema}__patch_at_uid_handler'](uid, update)

    # DELETE =========================
    @app.delete(
        '/{}'.format(raw_name_plural),
        tags=[raw_name_plural],
    )
    def delete_all_instances(token: str = Depends(oauth2_scheme)):
        check_token(token)
        return HANDLERS[f'{schema}__delete_all_instances_handler']()

    @app.delete(
        '/{}/{{uid}}'.format(raw_name_plural),
        tags=[raw_name_plural],
    )
    def delete_instance_by_uid(uid: str, token: str = Depends(oauth2_scheme)):
        check_token(token)
        return HANDLERS[f'{schema}__delete_instance_by_uid_handler'](uid)

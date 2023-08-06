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

from typing import Callable, Dict, List, Literal, Optional, Union

from cobblestone.database import session_scope

OrderingDirections = Union[Literal['asc'], Literal['desc']]


def list_instances_handler(db_schema: type) -> Callable:
    def _f(
        skip: int,
        limit: int,
        sort_by: Optional[str] = 'id',
        sort_dir: OrderingDirections = 'asc'
    ) -> List[Dict]:
        if hasattr(db_schema, 'before_read'):
            db_schema.before_read(multiple=True)
        results = []
        with session_scope() as session:
            req = session.query(db_schema)
            if sort_by is not None:
                order_clause = getattr(db_schema, sort_by)
                if sort_dir == 'desc':
                    order_clause = order_clause.desc()
                req = req.order_by(order_clause)
            for instance in req.offset(skip).limit(limit):
                results.append(instance.to_json(session))
                if hasattr(db_schema, 'after_read'):
                    instance.after_read()
        return results
    return _f


def get_instance_by_uid_handler(db_schema: type) -> Callable:
    def _f(uid: str) -> dict:
        if hasattr(db_schema, 'before_read'):
            db_schema.before_read(multiple=False)
        with session_scope() as session:
            instance = session.query(db_schema).filter_by(uid=uid).first()
            if instance:
                if hasattr(db_schema, 'after_read'):
                    instance.after_read()
                return instance.to_json(session)
            else:
                return None
    return _f

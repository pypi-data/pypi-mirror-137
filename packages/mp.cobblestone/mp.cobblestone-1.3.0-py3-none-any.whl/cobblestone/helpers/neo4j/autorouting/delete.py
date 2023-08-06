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

from typing import Callable

from cobblestone.database import session_scope


def delete_all_instances_handler(db_schema: type) -> Callable:
    def _f() -> None:
        if hasattr(db_schema, 'before_delete'):
            db_schema.before_delete(multiple=True)
        with session_scope() as session:
            for instance in db_schema.find_all():
                session.delete(instance)
                if hasattr(db_schema, 'after_delete'):
                    db_schema.after_delete()
    return _f


def delete_instance_by_uid_handler(db_schema: type) -> Callable:
    def _f(uid: str) -> None:
        if hasattr(db_schema, 'before_delete'):
            db_schema.before_delete(multiple=False)
        instance = db_schema.find_one(uid=uid)
        if instance:
            with session_scope() as session:
                session.delete(instance)
                if hasattr(db_schema, 'after_delete'):
                    db_schema.after_delete()
        else:
            return None
    return _f

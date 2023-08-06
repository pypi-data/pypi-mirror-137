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


def patch_at_uid_handler(db_schema: type) -> Callable:
    def _f(uid: str, update: dict) -> dict:
        if hasattr(db_schema, 'before_update'):
            db_schema.before_update()
        with session_scope() as session:
            instance = session.query(db_schema).filter_by(uid=uid).first()
            if instance:
                for k, v in update.items():
                    setattr(instance, k, v)
                if hasattr(db_schema, 'after_update'):
                    instance.after_update()
                return instance.to_json(session)
            else:
                return None
    return _f

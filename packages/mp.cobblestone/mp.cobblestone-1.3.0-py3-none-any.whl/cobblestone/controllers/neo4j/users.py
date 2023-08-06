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

from cobblestone.database import session_scope
from cobblestone.models.user import UserInDB
from cobblestone.helpers.utils import PRIMARY_KEY, create_uid


def get_user_by_uid(user_uid: str) -> dict:
    user = UserInDB.find_one(uid=user_uid)
    if user:
        return user.to_json()


def get_user(username: str) -> dict:
    user = UserInDB.find_one(username=username)
    if user:
        return user.to_json()
    else:
        return False


def create_user(data: dict) -> dict:
    data[PRIMARY_KEY] = create_uid()
    for k, v in getattr(UserInDB, '_constructors').items():
        data[k] = v(data)
    with session_scope() as session:
        instance = UserInDB(**data)
        session.create(instance)
        return instance.to_json()

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

from typing import Union

from py2neo.ogm import Model
from cobblestone.helpers.utils import (is_multi_rel,
                                       HAS_RELATIONSHIP_PROPERTIES,
                                       PRIMARY_KEY)


def find(klasses: Union[tuple, list], **query) -> Model:
    if not isinstance(klasses, (tuple, list)):
        klasses = [klasses]
    for klass in klasses:
        instance = klass.find_one(**query)
        if instance is not None:
            return instance
    return None


def find_by_id(klasses: Union[tuple, list], id: str) -> Model:
    if not isinstance(klasses, (tuple, list)):
        klasses = [klasses]
    query = {PRIMARY_KEY: id}
    return find(klasses, **query)


def get_connection_prop_name(prop_name: str, target_klass: Union[str, type, Model]) -> str:
    if isinstance(target_klass, Model):
        target_klass = target_klass.__class__.__name__
    elif isinstance(target_klass, type):
        target_klass = target_klass.__name__
    if '.' in target_klass:
        target_klass = target_klass.split('.')[-1]
    return f'{prop_name}__rel__{target_klass}'


def is_connected(instance: Model, other: Model, prop_name: str) -> bool:
    if not '__rel__' in prop_name:
        prop_name = get_connection_prop_name(prop_name, other)
    return any(x[0] == other for x in getattr(instance, prop_name)._related_objects)


def connect(
    instance: Model,
    other: Model,
    prop_name: str,
    prop_data: dict = {},
    force: bool = False
):
    # avoid recreating the connection, unless it is forced
    full_prop_name = get_connection_prop_name(prop_name, other)
    if is_connected(instance, other, full_prop_name) and not force:
        return
    rel = instance._relationships[prop_name]
    # if relationship data is enabled: add default values from model
    if HAS_RELATIONSHIP_PROPERTIES and (m := rel.get('model')):
        prop_data.update(m(**prop_data).dict())
    if is_multi_rel(rel):
        getattr(instance, full_prop_name).add(other, prop_data)
    else:
        a = getattr(instance, full_prop_name)
        a.clear()
        a.add(other, prop_data)


def disconnect(instance: Model, other: Model, prop_name: str):
    # ignore disconnection if there is already no connection!
    full_prop_name = get_connection_prop_name(prop_name, other)
    if not is_connected(instance, other, full_prop_name):
        return
    getattr(instance, full_prop_name).remove(other)

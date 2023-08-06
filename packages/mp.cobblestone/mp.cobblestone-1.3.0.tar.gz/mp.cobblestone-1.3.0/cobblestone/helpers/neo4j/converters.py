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
import inspect
import interchange
from typing import Any, Union

from pydantic import create_model
from pydantic.main import BaseModel
from py2neo.ogm import Model, Property, Related, RelatedTo, RelatedFrom

from cobblestone.database import db
from cobblestone.helpers.tools import get_connection_prop_name
from cobblestone.helpers.types import get_real_type
from cobblestone.helpers.utils import (apply_hooks,
                                       clean_up_class_name,
                                       get_class,
                                       make_rel_field,
                                       is_multi_rel,
                                       PRIMARY_KEY,
                                       RETURN_RELATIONSHIP_PROPERTIES)


DIRECT_TABLES = {}

PYDANTIC_TO_NEO4J_TYPES = {
    'relationship_any': Related,
    'relationship_to': RelatedTo,
    'relationship_from': RelatedFrom,
}


def json_encode(value):
    if type(value) == interchange.time.DateTime:
        return str(value)
    return value


class ExtendedModel(Model):

    def to_json(self: Model) -> dict:
        data = {k: json_encode(v) for k, v in dict(self.__node__).items()}
        for pname, pdata in self._relationships.items():
            rel_klass = pdata['target']
            if not isinstance(rel_klass, (tuple, list)):
                rel_klass = [rel_klass]
            for k in rel_klass:
                a = getattr(self, get_connection_prop_name(pname, k))
                related = list(a.triples())
                if RETURN_RELATIONSHIP_PROPERTIES:
                    if is_multi_rel(pdata):
                        res = []
                        for _, (label, props), target in related:
                            props['label'] = label
                            res.append({'item': target.to_json(), 'rel': props})
                        data[pname] = data.get(pname, []) + res
                    else:
                        _, (label, props), target = related[0]
                        props['label'] = label
                        data[pname] = {'item': target.to_json(), 'rel': props}
                else:
                    if is_multi_rel(pdata):
                        data[pname] = data.get(pname, []) + \
                            [target.to_json() for _, _, target in related]
                    else:
                        _, _, target = related[0]
                        data[pname] = target.to_json()
        return data

    def update(self: Model, update: dict) -> dict:
        self.__node__.update(**update)

    @classmethod
    def find_one(cls: type, **kwargs: Any) -> Model:
        return cls.match(db).where(**kwargs).first()

    @classmethod
    def find_all(cls: type, **kwargs: Any) -> Model:
        limit = kwargs.pop('limit', None)
        skip = kwargs.pop('skip', None)
        order_by = kwargs.pop('order_by', None)
        q = cls.match(db).where(**kwargs)
        if skip:
            q = q.skip(skip)
        if limit:
            q = q.limit(limit)
        if order_by:
            q = q.order_by(order_by)
        return list(q)


def PydanticToNeo4jParams(schema: dict, klass_params: dict) -> dict:
    klass_props = {}
    for pname, pdata in schema['properties'].items():
        a = klass_params[pname].annotation
        t = get_real_type(a)
        # ignore fields if they point to other models => we will create
        # relationships later on
        if inspect.isclass(t) and issubclass(t, BaseModel):
            continue
        if t == list and any(issubclass(x, BaseModel) for x in a.__args__):
            continue
        if t == Union and any(issubclass(x, BaseModel) for x in a.__args__):
            continue
        poptions = {}
        if 'default' in pdata:
            poptions['default'] = pdata['default']
        klass_props[pname] = Property(**poptions)
    return klass_props


def PydanticToORM(
    klass: BaseModel,
    collection: str = None,
    constructors: dict = {},
    relationships: dict = {},
    additional_fields: dict = {},
    hooks: dict = {},
    return_class: str = None
) -> Model:
    base_klass_name = clean_up_class_name(klass.schema()['title'])
    klass_name = base_klass_name + 'InDB'
    # prepare the "return class" friend-class for JSON response
    # payloads formatting
    if return_class is None:
        schemas_module = importlib.import_module(
            '.' + base_klass_name.lower(), 'cobblestone.models')
        if hasattr(schemas_module, base_klass_name + 'Full'):
            return_class = getattr(schemas_module, base_klass_name + 'Full')
        else:
            return_class = getattr(schemas_module, base_klass_name)

    # if relationships have properties: automatically wrap relationship fields
    # in additional "item" and "rel" keys
    # -> this will update the return class with fields that have the rel() wrapper
    if RETURN_RELATIONSHIP_PROPERTIES:
        props = {}
        f = klass.__fields__
        for r in relationships:
            props[r] = (make_rel_field(f[r]), ...)
        return_class = create_model('RelWrapped' + base_klass_name,
                                    __base__=return_class, **props)

    schema = klass.schema()

    # extract base parameters from the factory class
    klass_params = inspect.signature(klass).parameters
    klass_props = PydanticToNeo4jParams(schema, klass_params)
    if collection is None:
        collection = base_klass_name
    klass_props['__primarylabel__'] = collection

    # if there are relationships: for each, create the corresponding Neo4j
    # RelationshipManager (with optionally a parent abstract class in case
    # of multiple relationship target types)
    for pname, pdata in relationships.items():
        rel_klass = pdata['target']
        rel_type = PYDANTIC_TO_NEO4J_TYPES['relationship_' +
                                           pdata.get('direction', 'to')]
        if isinstance(rel_klass, (tuple, list)):
            for k in rel_klass:
                c = get_class(k)
                n = get_connection_prop_name(pname, c)
                klass_props[n] = rel_type(c, pdata['label'])
        else:
            if inspect.isclass(rel_klass) and issubclass(rel_klass, BaseModel):
                c = rel_klass
                rel_klass = rel_klass.__name__
            if '.' in rel_klass:
                c = get_class(rel_klass)
                rel_klass = rel_klass.split('.')[-1]
            n = get_connection_prop_name(pname, rel_klass)
            klass_props[n] = rel_type(c, pdata['label'])

    # add primary key field
    klass_props[PRIMARY_KEY] = Property()
    klass_props['__primarykey__'] = PRIMARY_KEY

    # add util info for further processing
    klass_props['_constructors'] = constructors
    klass_props['_relationships'] = relationships
    klass_props['_additional_fields'] = additional_fields
    klass_props['response_model'] = return_class
    # create the actual database ORM class
    neo4j_klass = type(klass_name, (ExtendedModel,), klass_props)

    # apply hooks by injecting "klass" or "instance"
    apply_hooks(neo4j_klass, hooks)

    DIRECT_TABLES[klass_name] = neo4j_klass
    return neo4j_klass


def wrap_additional_fields(schemas):
    for schema in schemas:
        db_schema = DIRECT_TABLES[schema + 'InDB']

        # add any supplementary fields
        for pname, pdata in db_schema._additional_fields.items():
            ptype = pdata['type']
            poptions = {}
            if pdata.get('required', True):
                poptions['required'] = True
            if (d := pdata.get('default', None)) is not None:
                poptions['default'] = d
            if isinstance(ptype, str) and ptype.startswith('$'):
                pklass = get_class(ptype.lstrip('$'))
                if pklass.__class__.__name__.endswith('InDB'):
                    ptype = getattr(pklass, 'response_model')
                else:
                    ptype = pklass
            else:
                ptype = get_real_type(ptype)
            if ptype in PYDANTIC_TO_NEO4J_TYPES:
                setattr(db_schema, pname, PYDANTIC_TO_NEO4J_TYPES[ptype](**poptions))

        # remove "_additional_fields" property from class
        # since it is not useful anymore
        delattr(db_schema, '_additional_fields')

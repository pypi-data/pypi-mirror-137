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
from mongoengine import DoesNotExist, MultipleObjectsReturned

from cobblestone.helpers.tools import create_relationship
from cobblestone.helpers.utils import (create_uid,
                                       format_ref_uid,
                                       format_ref_rel,
                                       invalid_input_data_exception,
                                       get_class,
                                       is_multi_rel,
                                       PRIMARY_KEY,
                                       HAS_RELATIONSHIP_PROPERTIES)


def create_instance_handler(
    schema: str,
    db_schema: type,
    full_schema: type
) -> Callable:
    def _f(data: dict) -> dict:
        if hasattr(db_schema, 'before_create'):
            db_schema.before_create()

        data = data.dict()
        pk = data.get(PRIMARY_KEY, None)
        if pk is None:
            data[PRIMARY_KEY] = create_uid()
        for k, v in getattr(db_schema, '_constructors').items():
            data[k] = v(data)
        for k, v in getattr(db_schema, '_relationships').items():
            linked_instances = []
            linked_schema = full_schema.schema()['properties'][k]
            rel_key = format_ref_uid(k)
            linked_uid = data.get(rel_key)
            cardinality = v.get('cardinality', 'ZeroOrMore')
            multi_rel = is_multi_rel(v)
            rel_model = v.get('model', None)
            if not linked_uid:
                dft = linked_schema.get('default')
                # error if we need at least one connection and we don't
                # have any (provided by the user or by the class defaults)
                if not cardinality.startswith('Zero') and dft is None:
                    raise invalid_input_data_exception
                else:
                    linked_uid = dft
            if isinstance(linked_uid, (list, tuple)) and len(linked_uid) == 0:
                continue
            linked_klass = v['target']
            if isinstance(linked_klass, str):
                linked_klass = [get_class(linked_klass)]
            elif isinstance(linked_klass, (tuple, list)):
                linked_klass = [get_class(k) for k in linked_klass]
            if isinstance(linked_uid, list):
                props = [] if not HAS_RELATIONSHIP_PROPERTIES else data.get(
                    format_ref_rel(k), [])
                for linked_k in linked_klass:
                    for i, x in enumerate(linked_k.objects(pk__in=linked_uid).all()):
                        p = props[i] if i < len(props) else {}
                        if rel_model is not None:
                            p.update(rel_model(**p).dict())
                        linked_instances.append((x, p))
            else:
                props = {} if not HAS_RELATIONSHIP_PROPERTIES else data.get(
                    format_ref_rel(k), {})
                if rel_model is not None:
                    props.update(rel_model(**props).dict())
                for linked_k in linked_klass:
                    try:
                        linked_instance = linked_k.objects(pk=linked_uid).get()
                        if linked_instance is not None:
                            linked_instances.append((linked_instance, props))
                    except (DoesNotExist, MultipleObjectsReturned):
                        pass
            if len(linked_instances) == 0 and cardinality.startswith('One'):
                raise invalid_input_data_exception
            data.pop(format_ref_rel(k), None)

            if multi_rel:
                data[rel_key] = [x[0] for x in linked_instances]
            else:
                data[rel_key] = linked_instances[0][0]
            if HAS_RELATIONSHIP_PROPERTIES:
                rel_val = data.get(rel_key)
                ref_rel = format_ref_rel(k)
                props = data.pop(ref_rel, {})
                rel_data = create_relationship(schema, rel_val, k, v, **props)
                if rel_data:
                    data[ref_rel] = rel_data
        instance = db_schema(**data).save()
        if hasattr(db_schema, 'after_create'):
            instance.after_create()
        return instance.to_json()
    return _f

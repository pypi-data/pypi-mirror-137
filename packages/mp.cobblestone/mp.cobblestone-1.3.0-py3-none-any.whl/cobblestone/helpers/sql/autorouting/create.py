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

import json
from typing import Callable

from cobblestone.database import session_scope
from cobblestone.helpers.converters import DIRECT_TABLES, ASSOCIATION_TABLES
from cobblestone.helpers.tools import find_by_id
from cobblestone.helpers.utils import (create_uid,
                                       clean_up_class_name,
                                       format_ref_uid,
                                       format_ref_rel,
                                       is_multi_rel,
                                       invalid_input_data_exception,
                                       get_class,
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
        linked_instances = []
        for k, v in getattr(db_schema, '_relationships').items():
            linked_schema = full_schema.schema()['properties'][k]
            linked_uid = data.get(format_ref_uid(k))
            cardinality = v.get('cardinality', 'ZeroOrMore')
            rel_model = v.get('model', None)
            uselist = is_multi_rel(v)
            if not linked_uid:
                dft = linked_schema.get('default')
                if dft is None:
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
                    other_klass_name = other.__class__.__name__
                    other_klass_tablename = other.__class__.__tablename__
                    link_klass_name = \
                        f'{DIRECT_TABLES[schema + "InDB"].__tablename__}' + \
                        '_to_' + \
                        f'{other_klass_tablename}'
                    link_klass = ASSOCIATION_TABLES[link_klass_name]
                    with session_scope() as session:
                        for i, x in enumerate(session.query(linked_k).filter(linked_k.uid.in_(linked_uid)).all()):
                            p = props[i] if i < len(props) else {}
                            p['label'] = v.get('label', '')
                            if rel_model is not None:
                                p.update(rel_model(**p).dict())
                            linked_instances.append(
                                (k, x.uid, other_klass_name, link_klass, uselist, p))
            else:
                props = {} if not HAS_RELATIONSHIP_PROPERTIES else data.get(
                    format_ref_rel(k), {})
                props['label'] = v.get('label', '')
                if rel_model is not None:
                    props.update(rel_model(**props).dict())
                other = None
                with session_scope() as session:
                    other = find_by_id(session, linked_klass, linked_uid)
                    if other is not None:
                        other_klass_name = other.__class__.__name__
                        other_klass_tablename = other.__class__.__tablename__
                        link_klass_name = \
                            f'{DIRECT_TABLES[schema + "InDB"].__tablename__}' + \
                            '_to_' + \
                            f'{other_klass_tablename}'
                        link_klass = ASSOCIATION_TABLES[link_klass_name]
                        linked_instances.append(
                            (k, getattr(other, PRIMARY_KEY), other_klass_name, link_klass, uselist, props))
            if len(linked_instances) == 0 and cardinality.startswith('One'):
                raise invalid_input_data_exception
            data.pop(format_ref_uid(k), None)
            data.pop(format_ref_rel(k), None)
        instance = db_schema(**data)
        with session_scope() as session:
            for k, uid, other_klass, link_klass, uselist, props in linked_instances:
                link_props = {}
                if HAS_RELATIONSHIP_PROPERTIES:
                    # link_props['data'] = json.dumps(props)
                    link_props.update(props)
                link_uid = format_ref_uid(clean_up_class_name(schema).lower())
                rel_link_uid = format_ref_uid(clean_up_class_name(other_klass).lower())
                link_props[link_uid] = getattr(instance, PRIMARY_KEY)
                link_props[rel_link_uid] = uid
                link = link_klass(**link_props)
                if uselist:
                    getattr(instance, f'{k}__rel__{other_klass}').append(link)
                else:
                    setattr(instance, f'{k}__rel__{other_klass}', link)
            session.add(instance)
            session.commit()
            if hasattr(db_schema, 'after_create'):
                instance.after_create()
            return instance.to_json(session)
    return _f

import os
from contextlib import contextmanager

from py2neo import Graph

NEO4J_USER = os.getenv('DB_USER')
NEO4J_PASSWORD = os.getenv('DB_PASSWORD')
NEO4J_HOST = os.getenv('DB_HOST', '0.0.0.0')
NEO4J_BOLT_PORT = os.getenv('DB_PORT', '7687')

print(f'Connecting to Neo4j DB (@{NEO4J_HOST}:{NEO4J_BOLT_PORT})')
db = Graph(f'bolt://{NEO4J_HOST}:{NEO4J_BOLT_PORT}', auth=(NEO4J_USER, NEO4J_PASSWORD))


def initialize_database_metadata():
    import cobblestone.models as all_schemas
    from cobblestone.helpers.converters import wrap_additional_fields
    wrap_additional_fields(all_schemas.__all__)


@contextmanager
def session_scope(autocommit=True):
    session = db.begin()
    try:
        yield session
        if autocommit:
            db.commit(session)
    except:
        session.rollback()
        raise

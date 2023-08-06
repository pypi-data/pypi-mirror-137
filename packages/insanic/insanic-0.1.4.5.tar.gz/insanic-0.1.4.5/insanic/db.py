import os

from sanic import Sanic
from tortoise import Tortoise, Model, fields, functions, queryset
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.backends.base.config_generator import generate_config
from tortoise.manager import Manager as ModelManager


__all__ = (
    'Model',
    'ModelManager',
    'fields',
    'functions',
    'queryset',
    'init_db_connection',
    'close_db_connection',
)

def get_db_connection() -> BaseDBAsyncClient:
    return Tortoise.get_connection('default')

async def init_db_connection() -> BaseDBAsyncClient:
    application = Sanic.get_app()
    database_url = application.config.DATABASE_URL

    # Building list of blueprints with `models.py`
    # to add them into list of modules for TortoiseORM
    blueprint_models = {}
    for blueprint_name in application.blueprints:
        if os.path.exists(f'src/{blueprint_name}/models.py'):
            blueprint_models[blueprint_name] = [f'{blueprint_name}.models']

    print(blueprint_models)

    # @TODO: Fix this ugly hack. Tortoise doesn't like empty modules so we trick it
    if len(blueprint_models.keys()) == 0:
        blueprint_models = {'models': {}}

    import json
    print(json.dumps(generate_config(database_url, blueprint_models), indent=2))

    await Tortoise.init(db_url=database_url, modules=blueprint_models)
    return get_db_connection()

async def close_db_connection() -> None:
    await Tortoise.close_connections()

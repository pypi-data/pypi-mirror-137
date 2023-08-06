import datetime
import inspect
import json
import logging
from typing import TYPE_CHECKING, Optional, cast

import jwt
import redis

from nawah.classes import JSONEncoder
from nawah.config import Config
from nawah.enums import Event

if TYPE_CHECKING:
    from nawah.base_module import BaseModule
    from nawah.classes import CACHE, NAWAH_ENV, NAWAH_EVENTS, NAWAH_QUERY

logger = logging.getLogger('nawah')


def _generate_cache_key(
    cache: 'CACHE',
    method: str,
    module: 'BaseModule',
    skip_events: 'NAWAH_EVENTS',
    env: 'NAWAH_ENV',
    query: 'NAWAH_QUERY',
) -> Optional[str]:
    if Event.CACHE in skip_events or not cache:
        return None

    condition_params = {
        'skip_events': skip_events,
        'env': env,
        'query': query,
    }

    if not cache.condition(
        **{
            param: condition_params[param]
            for param in inspect.signature(cache.condition).parameters
        }
    ):
        return None

    try:
        if not Config._sys_cache.get(cache.channel):
            Config._sys_cache.set(cache.channel, '.', {})
        try:
            Config._sys_cache.get(cache.channel, f'.{module.module_name}')
        except redis.exceptions.ResponseError:
            Config._sys_cache.set(cache.channel, f'.{module.module_name}', {})
        try:
            Config._sys_cache.get(cache.channel, f'.{module.module_name}.{method}')
        except redis.exceptions.ResponseError:
            Config._sys_cache.set(
                cache.channel,
                f'.{module.module_name}.{method}',
                {},
            )
    except redis.exceptions.ConnectionError:
        logger.error(
            'Connection with Redis server \'%s\' failed. Skipping Cache Workflow.',
            Config.cache_server,
        )

    cache_key = {
        'query': JSONEncoder().encode(query._query),
        'special': JSONEncoder().encode(query._special),
        'extn': Event.EXTN in skip_events,
        'user': env['session']['user']['_id'] if cache.user_scoped else None,
    }

    cache_key_jwt = jwt.encode(cache_key, '_').split('.')[1]

    return cache_key_jwt


def _call_cache(cache: 'CACHE', method: str, module: 'BaseModule', cache_key: str):
    try:
        return Config._sys_cache.get(
            cache.channel,
            f'.{module.module_name}.{method}.{cache_key}',
        )

    except redis.exceptions.ResponseError:
        return

    except redis.exceptions.ConnectionError:
        logger.error(
            'Connection with Redis server \'%s\' failed. Skipping Cache Workflow.',
            Config.cache_server,
        )
        return


def _call_method(
    cache: 'CACHE',
    method: str,
    module: 'BaseModule',
    skip_events: 'NAWAH_EVENTS',
    env: 'NAWAH_ENV',
    query: 'NAWAH_QUERY',
):
    cache_key = _generate_cache_key(
        cache=cache,
        method=method,
        module=module,
        skip_events=skip_events,
        env=env,
        query=query,
    )
    call_cache = None
    if cache_key:
        cache_key = cast(str, cache_key)
        call_cache = _call_cache(
            cache=cache, method=method, module=module, cache_key=cache_key
        )

    async def _method(skip_events, env, query, doc):
        if call_cache:
            return call_cache

        module_method = getattr(module, f'_method_{method}')

        method_params = {
            'skip_events': skip_events,
            'env': env,
            'query': query,
            'doc': doc,
        }

        results = await module_method(
            **{
                param: method_params[param]
                for param in inspect.signature(module_method).parameters
            }
        )

        if cache_key:
            results['args']['cache_key'] = cache_key
            results['args']['cache_time'] = datetime.datetime.utcnow().isoformat()
            try:
                Config._sys_cache.set(
                    cache.channel,
                    f'.{module.module_name}.{method}.{results["args"]["cache_key"]}',
                    json.loads(JSONEncoder().encode(results)),
                )
            except redis.exceptions.ConnectionError:
                logger.error(
                    'Connection with Redis server \'%s\' failed. Skipping Cache Workflow.',
                    Config.cache_server,
                )
            del results['args']['cache_time']

        return results

    return _method

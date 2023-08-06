import logging
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

from nawah.classes import ATTR, NAWAH_ENV, Query
from nawah.config import Config

from ._query import _compile_query
from ._read import _process_results_doc

logger = logging.getLogger('nawah')


async def watch(
    *,
    env: NAWAH_ENV,
    collection_name: str,
    attrs: Dict[str, ATTR],
    query: Query,
    skip_extn: bool = False,
) -> AsyncGenerator[Dict[str, Any], Dict[str, Any]]:
    aggregate_query = _compile_query(
        collection_name=collection_name, attrs=attrs, query=query, watch_mode=True
    )[4]

    collection = env['conn'][Config.data_name][collection_name]

    logger.debug('Preparing generator at Data')
    async with collection.watch(
        pipeline=aggregate_query, full_document='updateLookup'
    ) as stream:
        yield {'stream': stream}
        async for change in stream:
            logger.debug(f'Detected change at Data: {change}')

            oper = change['operationType']
            if oper in ['insert', 'replace', 'update']:
                if oper == 'insert':
                    oper = 'create'
                elif oper == 'replace':
                    oper = 'update'
                doc = await _process_results_doc(
                    env=env,
                    collection=collection,
                    attrs=attrs,
                    doc=change['fullDocument'],
                    skip_extn=skip_extn,
                )
                model = doc
            elif oper == 'delete':
                model = {'_id': change['documentKey']['_id']}

            yield {'count': 1, 'oper': oper, 'docs': [model]}

    logger.debug('changeStream has been close. Generator ended at Data')

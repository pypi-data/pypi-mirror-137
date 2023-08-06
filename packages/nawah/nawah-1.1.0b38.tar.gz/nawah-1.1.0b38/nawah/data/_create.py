from typing import Any, Dict

from nawah.classes import ATTR, NAWAH_DOC, NAWAH_ENV
from nawah.config import Config


async def create(
    *,
    env: NAWAH_ENV,
    collection_name: str,
    attrs: Dict[str, ATTR],
    doc: NAWAH_DOC,
) -> Dict[str, Any]:
    collection = env['conn'][Config.data_name][collection_name]
    results = await collection.insert_one(doc)
    _id = results.inserted_id
    return {'count': 1, 'docs': [{'_id': _id}]}

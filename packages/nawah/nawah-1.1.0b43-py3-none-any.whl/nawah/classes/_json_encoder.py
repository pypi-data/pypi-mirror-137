import datetime
import json

from bson import ObjectId


class JSONEncoderStr(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, datetime.datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return True

        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


JSONEncoderStrIns = JSONEncoderStr()


class JSONEncoderDict(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return {'$oid': str(o)}

        if isinstance(o, datetime.datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return True

        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


JSONEncoderDictIns = JSONEncoderDict()


def JSONEncoder(object_id_dict=False) -> json.JSONEncoder:
    if object_id_dict:
        return JSONEncoderDictIns

    return JSONEncoderStrIns

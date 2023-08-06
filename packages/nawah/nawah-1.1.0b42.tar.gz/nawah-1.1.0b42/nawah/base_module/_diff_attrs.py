from nawah.classes import ATTR

diff_attrs = {
    'user': ATTR.ID(),
    'doc': ATTR.ID(),
    'attrs': ATTR.KV_DICT(key=ATTR.STR(), val=ATTR.ANY()),
}

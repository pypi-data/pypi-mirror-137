'''Provides Core Nawah module'''

from nawah.base_module import BaseModule
from nawah.classes import ATTR, METHOD, PERM
from nawah.config import Config


class Core(BaseModule):
    '''`Core` module provides access to ADMIN user to fetch `Nawah` instance.'''

    methods = {
        'retrieve_config': METHOD(
            permissions=[PERM(privilege='admin')],
            query_args={'config_attr': ATTR.STR()},
        ),
    }

    async def retrieve_config(self, query):
        '''Returns current value of provided `Config Attr`'''

        return self.status(
            status=200,
            msg='Config Attr value retrieved.',
            args={'value': getattr(Config, query['config_attr'][0])},
        )

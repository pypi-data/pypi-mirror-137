'''Provides `reset_cache` Utility'''

from nawah.config import Config


def reset_cache(channel: str) -> None:
    '''Resets specific cache `channel` by deleting it from active Redis db'''

    Config._sys_cache.delete(channel, '.')

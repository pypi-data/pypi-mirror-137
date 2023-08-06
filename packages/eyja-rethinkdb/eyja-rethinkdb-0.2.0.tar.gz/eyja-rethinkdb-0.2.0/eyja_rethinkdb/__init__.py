from eyja.interfaces.plugins import BasePlugin
from eyja.constants.types import PluginTypes

from .client import RethinkDBClient


class RethinkDBPlugin(BasePlugin):
    name = 'rethinkdb'
    plugin_type = PluginTypes.STORAGE_CLIENT

    @classmethod
    async def run(cls, **params):
        client = RethinkDBClient(params)
        await client.init()

        return client

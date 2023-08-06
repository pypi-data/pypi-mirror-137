from eyja.interfaces.plugins import BasePlugin
from eyja.constants.types import PluginTypes

from .client import FileDBClient


class FileDBPlugin(BasePlugin):
    name = 'filedb'
    plugin_type = PluginTypes.STORAGE_CLIENT

    @classmethod
    async def run(cls, **params):
        client = FileDBClient(params)
        await client.init()

        return client

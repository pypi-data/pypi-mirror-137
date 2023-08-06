import uuid

from eyja.interfaces.db import BaseStorageClient

from eyja_filedb.db import Connection

from .config import FileDBConfig


class FileDBClient(BaseStorageClient):
    _connection = None
    _config: FileDBConfig
    _config_cls = FileDBConfig

    async def init(self):
        self._connection = Connection(self._config.path)
        await self._connection.init(self._config.db)
        self._buckets.extend(self._config.db)

    async def save(self, obj, object_space, object_type):
        if not obj.object_id:
            obj.object_id = str(uuid.uuid4())

            await self._connection.create_object(object_space, object_type, obj)
        else:
            await self._connection.update_object(object_space, object_type, obj.object_id, obj.dict())

    async def delete(self, obj, object_space, object_type):
        pass

    async def delete_all(self, obj, object_space, object_type, filter):
        pass

    async def get(self, obj_cls, object_space, object_type, object_id):
        return self._connection.get_object(object_space, object_type, object_id)

    async def get_from_index(self, obj_cls, object_space, object_type, value, index):
        pass

    async def find(self, obj_cls, object_space, object_type, filter):
        return self._connection.find_objects(object_space, object_type, filter)

    async def count(self, obj_cls, object_space, object_type, filter):
        pass

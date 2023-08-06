import json
import aiofiles

from pathlib import Path
from typing import List
from eyja.utils import EyjaJSONEncoder

from pydantic import BaseModel

from .db_batch import DBBatch


class Connection:
    _batch: DBBatch

    def __init__(self, path):
        self.path = path

    async def init(self, db_list: List[str]):
        db_file = Path(self.path)
        if db_file.is_file():
            async with aiofiles.open(self.path, 'r') as fp:
                self._batch = DBBatch(
                    **json.loads(await fp.read())
                )
        else:
            self._batch = DBBatch()

        for db in db_list:
            self._batch.init_db(db)

        await self.save_db()

    async def save_db(self):
        async with aiofiles.open(self.path, 'w') as fp:
            await fp.write(
                json.dumps(
                    self._batch.dict(),
                    cls=EyjaJSONEncoder,
                    indent=2,
                )
            )

    async def create_object(self, db, table, obj):
        self._batch.get_db(db).create_object(table, obj)
        await self.save_db()

    def get_object(self, db, table, object_id):
        return self._batch.get_db(db).get_object(table, object_id)

    async def update_object(self, db, table, object_id, obj):
        print(db, table, object_id, obj)

    def find_objects(self, db, table, filter):
        return self._batch.get_db(db).find_objects(table, filter)

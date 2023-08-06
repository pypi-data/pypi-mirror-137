from typing import List, Optional, Dict

from pydantic import BaseModel

from .db import DB


class DBBatch(BaseModel):
    db: Optional[Dict[str, DB]] = {}

    def init_db(self, db_name):
        if db_name in self.db:
            return

        self.db[db_name] = DB()

    def get_db(self, db_name) -> DB:
        if db_name in self.db:
            return self.db[db_name]

        db = DB()
        self.db[db_name] = db
        return db

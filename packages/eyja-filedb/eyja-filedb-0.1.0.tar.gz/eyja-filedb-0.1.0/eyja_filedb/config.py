from typing import List, Optional

from pydantic import BaseModel


class FileDBConfig(BaseModel):
    path: str
    db: List[str] = []

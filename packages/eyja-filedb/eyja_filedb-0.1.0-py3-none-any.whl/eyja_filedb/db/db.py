from typing import Optional, Dict

from pydantic import BaseModel

from .table import Table

class DB(BaseModel):
    tables: Optional[Dict[str, Table]] = {}

    def get_table(self, table_name, model_cls = None) -> Table:
        if table_name in self.tables:
            return self.tables[table_name]

        table = Table(model_cls=model_cls)
        self.tables[table_name] = table
        return table

    def create_object(self, table_name, obj):
        model_cls = f'{obj.__class__.__module__}.{obj.__class__.__qualname__}'
        table = self.get_table(table_name, model_cls)
        table.create_object(obj)

    def get_object(self, table_name, object_id):
        table = self.get_table(table_name)
        return table.get_object(object_id)

    def find_objects(self, table_name, filter):
        table = self.get_table(table_name)
        return table.find_objects(filter)

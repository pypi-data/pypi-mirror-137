import importlib

from typing import Optional, List, Any, Type

from eyja.interfaces.db import BaseStorageModel

from pydantic import BaseModel


class Table(BaseModel):
    model_cls: str
    objects: Optional[List[BaseModel]] = []

    def __init__(self, **data: Any) -> None:
        models_classes = BaseStorageModel.__subclasses__()
        objects_completed = False

        if 'objects' in data:
            objects_data = data['objects']

            model_cls = self.get_model_cls(data['model_cls'])
            if model_cls:
                data['objects'] = [model_cls(**object_data) for object_data in objects_data]
                objects_completed = True

        if not objects_completed:
            data['objects'] = []

        super().__init__(**data)

    def get_model_cls(self, model_cls_name) -> Type[BaseStorageModel]:
        models_classes = BaseStorageModel.__subclasses__()
        for model_cls in models_classes:
                model_class_name = f'{model_cls.__module__}.{model_cls.__qualname__}'
                if model_class_name == model_cls_name:
                    return model_cls

        return None

    def create_object(self, obj):
        self.objects.append(obj)

    def get_object(self, object_id):
        for obj in self.objects:
            if obj.object_id == object_id:
                return obj

    def find_objects(self, filter):
        result = []
        for obj in self.objects:
            finded_obj = False

            for filter_name, filter_value in filter.fields.items():
                if hasattr(obj, filter_name):
                    finded_obj = getattr(obj, filter_name) == filter_value
            
            if finded_obj:
                result.append(obj)
        
        return result

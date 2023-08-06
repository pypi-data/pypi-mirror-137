from typing import List, Type, Any

from eyja.interfaces.db import (
    BaseStorageModel,
    DataFilter,
)
from eyja.errors import (
    ObjectNotFoundError,
    NotAllowedError,
    DynamicFieldNotFoundError,
)

from .base_operator import BaseModelOperator


class ModelOperator(BaseModelOperator):
    @classmethod
    async def create(cls, data: dict, **kwargs) -> BaseStorageModel:
        for protected_field in cls.model._protected_fields:
            if protected_field in data:
                data.pop(protected_field)

        obj = cls.model(**data)
        await obj.save()
        return obj

    @classmethod
    async def get(cls, object_id: str, **kwargs) -> BaseStorageModel:
        obj = await cls.model.get(object_id)
        if not obj:
            raise ObjectNotFoundError()
        return obj

    @classmethod
    async def get_dynamic_field(cls, object_id: str, dynamic_field: str, **kwargs) -> Any:
        obj = await cls.model.get(object_id)

        if not obj:
            raise ObjectNotFoundError()

        if dynamic_field not in obj._dynamic_fields:
            raise NotAllowedError()

        try:
            field = getattr(obj, dynamic_field)
            return await field()
        except:
            raise DynamicFieldNotFoundError()

    @classmethod
    async def delete(cls, object_id: str, **kwargs):
        obj = await cls.model.get(object_id)
        if not obj:
            raise ObjectNotFoundError()
        await obj.delete()

    @classmethod
    async def update(cls, object_id: str, data: dict, **kwargs) -> BaseStorageModel:
        obj = await cls.model.get(object_id)
        if not obj:
            raise ObjectNotFoundError()
        obj.update(data)
        await obj.save()
        return obj

    @classmethod
    async def find(cls, filter: dict, **kwargs) -> List[BaseStorageModel]:
        return await cls.model.find(DataFilter.from_dict(filter))

    @classmethod
    async def count(cls, filter: dict, **kwargs) -> int:
        return await cls.model.count(filter)


def create_model_operator(model_cls: Type[BaseStorageModel]) -> ModelOperator:
    class operator(ModelOperator):
        model = model_cls

    return operator

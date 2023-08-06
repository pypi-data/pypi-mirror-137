from typing import List, Type

from eyja.interfaces.db import (
    BaseStorageModel,
    DataFilter,
)
from eyja.errors import ObjectNotFoundError


async def get_for_user(
    model_cls: Type[BaseStorageModel],
    object_id: str,
    user: BaseStorageModel
) -> BaseStorageModel:
    items = await model_cls.find({
        'object_id': object_id,
        'user_id': user.object_id,
    })

    if len(items) < 1:
        raise ObjectNotFoundError(
            message=object_id,
        )

    return items[0]

async def find_for_user(
    model_cls: Type[BaseStorageModel],
    filter: DataFilter,
    user: BaseStorageModel
) -> List[BaseStorageModel]:
    filter.fields['user_id'] = user.object_id

    return await model_cls.find(filter)

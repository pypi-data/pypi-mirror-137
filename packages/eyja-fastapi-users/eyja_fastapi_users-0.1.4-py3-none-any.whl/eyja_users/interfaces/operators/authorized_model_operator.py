from eyja.interfaces.operators import BaseModelOperator
from eyja.interfaces.db import BaseStorageModel

from eyja_users.helpers import (
    get_for_user,
    find_for_user,
)


class AuthorizedModelOperator(BaseModelOperator):
    @classmethod
    async def get_for_user(cls, object_id: str, user: BaseStorageModel):
        return await get_for_user(cls.model, object_id, user)

    @classmethod
    async def find_for_user(cls, filter, user: BaseStorageModel):
        return await find_for_user(cls.model, filter, user)

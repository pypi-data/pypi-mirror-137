from eyja.interfaces.db import BaseStorageModel
from eyja.utils import load_model

from eyja_users.errors import *
from eyja_users.models import (
    User,
    ConfirmToken,
)
from eyja_users.operators import ConfirmTokenOperator


class ConfirmProcess:
    user_model: BaseStorageModel
    confirm_token_model: BaseStorageModel

    @classmethod
    def init(cls):
        cls.user_model = load_model('users.model', User)
        cls.confirm_token_model = load_model('users.confirm_tokens.model', ConfirmToken)

    @classmethod
    async def run(cls, **params):
        cls.init()

        confirm_token_header = params.get('confirm_token', None)
        confirm_tokens = await cls.confirm_token_model.find({
            'token': confirm_token_header,
            'token_type': ConfirmTokenOperator.types.AUTH,
        })

        if len(confirm_tokens) < 1:
            raise UserNotFoundError(
                f'Confirm token is not found'
            )

        user = await cls.user_model.get(confirm_tokens[0].user_id)
        user.is_active = True
        await user.save()

        await confirm_tokens[0].delete()

        return user

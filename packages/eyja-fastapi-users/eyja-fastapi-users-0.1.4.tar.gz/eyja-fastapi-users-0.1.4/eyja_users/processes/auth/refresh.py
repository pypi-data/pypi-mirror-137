from eyja.interfaces.db import BaseStorageModel
from eyja.utils import load_model

from eyja_users.errors import *
from eyja_users.models import RefreshToken
from eyja_users.operators import (
    RefreshTokenOperator,
    AccessTokenOperator,
)


class RefreshProcess:
    refresh_token_model: BaseStorageModel

    @classmethod
    def init(cls):
        cls.refresh_token_model = load_model('users.refresh_tokens.model', RefreshToken)

    @classmethod
    async def run(cls, **params):
        cls.init()

        refresh_token_header = params.get('refresh_token', None)
        refresh_tokens = await cls.refresh_token_model.find({
            'token': refresh_token_header,
            'status': RefreshTokenOperator.statuses.ACTIVE,
        })
        if len(refresh_tokens) < 1:
            raise UserNotFoundError(
                f'Refresh token is not found'
            )

        return await AccessTokenOperator.create_token(refresh_tokens[0])

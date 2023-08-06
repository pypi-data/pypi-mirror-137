from eyja.interfaces.db import BaseStorageModel
from eyja.hubs.config_hub import ConfigHub
from eyja.utils import load_model

from eyja_email.operators import EmailOperator

from eyja_users.errors import *
from eyja_users.models import (
    User,
    AccessToken,
    RefreshToken,
    ConfirmToken,
)
from eyja_users.operators import (
    UserOperator,
    ConfirmTokenOperator,
    RefreshTokenOperator,
    AccessTokenOperator,
)


class UnauthorizationProcess:
    access_token_model: BaseStorageModel
    refresh_token_model: BaseStorageModel

    @classmethod
    def init(cls):
        cls.access_token_model = load_model('users.access_tokens.model', AccessToken)
        cls.refresh_token_model = load_model('users.refresh_tokens.model', RefreshToken)

    @classmethod
    async def run(cls, **params):
        cls.init()

        access_token = params.get('access_token')

        refresh_tokens = await cls.refresh_token_model.find({
            'object_id': access_token.refresh_token_id,
            'status': RefreshTokenOperator.statuses.ACTIVE,
        })
        if len(refresh_tokens) < 1:
            raise UserNotFoundError(
                f'Refresh token is not found'
            )

        refresh_tokens[0].status = RefreshTokenOperator.statuses.CANCELED
        await refresh_tokens[0].save()

        await cls.access_token_model.delete_all({
            'refresh_token_id': refresh_tokens[0].object_id,
        })

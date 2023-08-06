from eyja.interfaces.db import DataFilter
from eyja.utils import random_string, load_model

from eyja_users.models import ConfirmToken, User

from .types import ConfirmTokenTypes
from .constants import ConfirmTokenConstants


class ConfirmTokenOperator:
    types = ConfirmTokenTypes
    constants = ConfirmTokenConstants

    @classmethod
    async def create_token(cls, token_type, user):
        confirm_token_model = load_model('users.confirm_tokens.model', ConfirmToken)
        
        confirm_token = confirm_token_model(
            token=random_string(
                prefix=cls.constants.TOKEN_PREFIX,
                length=cls.constants.TOKEN_LENGTH,
            ),
            token_type=token_type,
            user_id=user.object_id,
        )

        await confirm_token.save()

        return confirm_token

    @classmethod
    async def verify_token(cls, token_type, token):
        confirm_token_model = load_model('users.confirm_tokens.model', ConfirmToken)
        user_model = load_model('users.model', User)

        filter = DataFilter(fields={
            'token': token,
            'token_type': token_type,
        })

        confirm_tokens = await confirm_token_model.find(filter)
        if len(confirm_tokens) < 1:
            return None

        await confirm_tokens[0].delete()

        return await user_model.get(confirm_tokens[0].user_id)

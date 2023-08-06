from eyja.utils import random_string, load_model

from eyja_users.models import AccessToken

from .constants import AccessTokenConstants


class AccessTokenOperator:
    constants = AccessTokenConstants

    @classmethod
    async def create_token(cls, refresh_token):
        access_token_model = load_model('users.access_tokens.model', AccessToken)

        access_token = access_token_model(
            token=random_string(
                prefix=cls.constants.TOKEN_PREFIX,
                length=cls.constants.TOKEN_LENGTH,
            ),
            refresh_token_id=refresh_token.object_id,
            user_id=refresh_token.user_id,
        )

        await access_token.save()

        return access_token

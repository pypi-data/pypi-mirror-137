from eyja.hubs.config_hub import ConfigHub
from eyja.utils import random_string, load_model

from eyja_users.models import RefreshToken

from .statuses import RefreshTokenStatuses
from .constants import RefreshTokenConstants


class RefreshTokenOperator:
    statuses = RefreshTokenStatuses
    constants = RefreshTokenConstants

    @classmethod
    async def create_token(cls, user, status=RefreshTokenStatuses.ACTIVE):
        refresh_token_model = load_model('users.refresh_tokens.model', RefreshToken)

        refresh_token = refresh_token_model(
            token=random_string(
                prefix=cls.constants.TOKEN_PREFIX,
                length=cls.constants.TOKEN_LENGTH,
            ),
            status=status,
            user_id=user.object_id,
        )

        await refresh_token.save()

        return refresh_token

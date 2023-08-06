from eyja.hubs.config_hub import ConfigHub

from eyja_users.errors import *
from eyja_users.operators import (
    UserOperator,
    RefreshTokenOperator,
    AccessTokenOperator,
)


class AuthorizationProcess:
    login_field: str

    @classmethod
    def init(cls):
        cls.login_field = ConfigHub.get('users.login_field', 'email')

    @classmethod
    async def run(cls, **params):
        cls.init()

        login_field_value = params.get(cls.login_field, None)
        password = params.get('password', None)

        if not login_field_value:
            raise MissingRequiredFieldError(
                f'Required field "{cls.login_field}" is missing'
            )

        if not password:
            raise MissingRequiredFieldError(
                f'Required field "password" is missing'
            )

        user = await UserOperator.authenticate(login_field_value, password)
        if not user:
            raise UserNotFoundError(
                f'User is not found'
            )

        refresh_token = await RefreshTokenOperator.create_token(user)
        access_token = await AccessTokenOperator.create_token(refresh_token)

        return [user, refresh_token, access_token]

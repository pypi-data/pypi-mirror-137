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


class UserProcess:
    @classmethod
    async def registration(cls, password:str = None, **params):
        login_field = ConfigHub.get('users.login_field', 'email')
        confirm_registration = ConfigHub.get('users.confirm_registration', True)
        use_email = ConfigHub.get('users.use_email', True)
        user_model = load_model('users.model', User)

        login_field_value = params.get(login_field, None)

        if not login_field_value:
            raise MissingRequiredFieldError(
                f'Required field "{login_field}" is missing'
            )

        exists_users = await user_model.find({login_field: login_field_value})
        if len(exists_users) > 0:
            raise UserAlreadyExistsError(
                f'User "{login_field_value}" already exists'
            )

        params['is_active'] = not confirm_registration
        params['is_admin'] = False

        user = await UserOperator.create_user(password, **params)

        if use_email:
            if confirm_registration:
                confirm_token = await ConfirmTokenOperator.create_token(
                    ConfirmTokenOperator.types.AUTH,
                    user,
                )

                email = await EmailOperator.create(
                    subject=ConfigHub.get('users.email.registration.subject','Successful registration'),
                    sender=ConfigHub.get('users.email.sender'),
                    sender_name=ConfigHub.get('users.email.sender_name'),
                    recipient=user.email,
                    template=ConfigHub.get('users.email.registration.template', 'registration.j2'),
                    message_data={
                        'confirm_token': confirm_token,
                        'user': user,
                    }
                )
            else:
                email = await EmailOperator.create(
                    subject=ConfigHub.get('users.email.registration.subject','Successful registration'),
                    sender=ConfigHub.get('users.email.sender'),
                    sender_name=ConfigHub.get('users.email.sender_name'),
                    recipient=user.email,
                    template=ConfigHub.get('users.email.registration.template', 'registration.j2'),
                    message_data={
                        'user': user,
                    }
                )

            await EmailOperator.send(email)

        return user

    @classmethod
    async def confirm(cls, **params):
        user_model = load_model('users.model', User)
        confirm_token_model = load_model('users.confirm_tokens.model', ConfirmToken)

        confirm_token_header = params.get('confirm_token', None)
        confirm_tokens = await confirm_token_model.find({
            'token': confirm_token_header,
            'token_type': ConfirmTokenOperator.types.AUTH,
        })
        if len(confirm_tokens) < 1:
            raise UserNotFoundError(
                f'Confirm token is not found'
            )

        user = await user_model.get(confirm_tokens[0].user_id)
        user.is_active = True
        await user.save()

        await confirm_tokens[0].delete()

        return user

    @classmethod
    async def authorization(cls, **params):
        login_field = ConfigHub.get('users.login_field', 'email')
        login_field_value = params.get(login_field, None)
        password = params.get('password', None)

        if not login_field_value:
            raise MissingRequiredFieldError(
                f'Required field "{login_field}" is missing'
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

    @classmethod
    async def refresh(cls, **params):
        refresh_token_model = load_model('users.refresh_tokens.model', RefreshToken)

        refresh_token_header = params.get('refresh_token', None)
        refresh_tokens = await refresh_token_model.find({
            'token': refresh_token_header,
            'status': RefreshTokenOperator.statuses.ACTIVE,
        })
        if len(refresh_tokens) < 1:
            raise UserNotFoundError(
                f'Refresh token is not found'
            )

        return await AccessTokenOperator.create_token(refresh_tokens[0])

    @classmethod
    async def unauthorization(cls, **params):
        access_token_header = params.get('access_token', None)
        access_token_model = load_model('users.access_tokens.model', AccessToken)
        refresh_token_model = load_model('users.refresh_tokens.model', RefreshToken)

        access_tokens = await access_token_model.find({'token': access_token_header})
        if len(access_tokens) < 1:
            raise UserNotFoundError(
                f'Access token is not found'
            )

        refresh_tokens = await refresh_token_model.find({
            'object_id': access_tokens[0].refresh_token_id,
            'status': RefreshTokenOperator.statuses.ACTIVE,
        })
        if len(refresh_tokens) < 1:
            raise UserNotFoundError(
                f'Refresh token is not found'
            )

        refresh_tokens[0].status = RefreshTokenOperator.statuses.CANCELED
        await refresh_tokens[0].save()

        await access_token_model.delete_all({
            'refresh_token_id': refresh_tokens[0].object_id,
        })

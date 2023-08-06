from eyja.interfaces.db import BaseStorageModel
from eyja.hubs.config_hub import ConfigHub
from eyja.utils import load_model

from eyja_email.operators import EmailOperator

from eyja_users.errors import *
from eyja_users.models import User
from eyja_users.operators import (
    UserOperator,
    ConfirmTokenOperator,
)


class RegistrationProcess:
    login_field: str
    confirm_registration: bool
    use_email: bool
    user_model: BaseStorageModel

    @classmethod
    def init(cls):
        cls.login_field = ConfigHub.get('users.login_field', 'email')
        cls.confirm_registration = ConfigHub.get('users.confirm_registration', True)
        cls.use_email = ConfigHub.get('users.use_email', True)
        cls.user_model = load_model('users.model', User)

    @classmethod
    async def send_email(cls, user):
        if cls.use_email:
            if cls.confirm_registration:
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

    @classmethod
    async def run(cls, **params):
        cls.init()

        login_field_value = params.get(cls.login_field, None)
        if not login_field_value:
            raise MissingRequiredFieldError(
                f'Required field "{cls.login_field}" is missing'
            )

        if not params.get('password', None):
            raise MissingRequiredFieldError(
                f'Required field "password" is missing'
            )

        exists_users = await cls.user_model.find({cls.login_field: login_field_value})
        if len(exists_users) > 0:
            raise UserAlreadyExistsError(
                f'User "{login_field_value}" already exists'
            )

        params['is_active'] = not cls.confirm_registration
        params['is_admin'] = False

        user = await UserOperator.create_user(**params)

        await cls.send_email(user)

        return user

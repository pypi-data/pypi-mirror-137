from eyja.interfaces.db import DataFilter
from eyja.hubs.config_hub import ConfigHub
from eyja.utils import load_model

from eyja_users.models import User


class UserOperator:
    @classmethod
    async def create_user(cls, password:str, **params):
        user_model = load_model('users.model', User)

        params.setdefault('is_active', False)
        params.setdefault('is_admin', False)

        user = user_model(**params)
        user.set_password(password)
        await user.save()

        return user

    @classmethod
    async def create_admin(cls, password:str, **params):
        params['is_active'] = True
        params['is_admin'] = True

        return await cls.create_user(password, **params)

    @classmethod
    async def authenticate(cls, login, password):
        login_field = ConfigHub.get('users.login_field', 'email')
        user_model = load_model('users.model', User)

        filter = DataFilter(
            fields={
                login_field: login,
                'is_active': True,
            }
        )

        users = await user_model.find(filter)
        if len(users) > 0 and users[0].check_password(password):
            return users[0]

        return None

    @classmethod
    async def get_user(cls, object_id: str):
        user_model = load_model('users.model', User)

        return await user_model.get(object_id)

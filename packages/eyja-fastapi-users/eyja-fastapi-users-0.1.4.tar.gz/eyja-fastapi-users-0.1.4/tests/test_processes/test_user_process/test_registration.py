import aioredis
import json
import html_to_json

from unittest import IsolatedAsyncioTestCase

from rethinkdb import r

from eyja.main import Eyja
from eyja.utils import render_template

from eyja_email.models import Email

from eyja_users.processes import UserProcess
from eyja_users.models import User, ConfirmToken
from eyja_users.errors import *


class UserRegistrationTest(IsolatedAsyncioTestCase):
    redis_url = 'redis://localhost:30002/4'

    async def test_registration_wrong_username_field(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config.yml')

        with self.assertRaises(MissingRequiredFieldError):
            await UserProcess.registration(
                username='test0@test.com',
                password='passTeSt123'
            )

    async def test_registration_duplicate_user(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config.yml')

        await UserProcess.registration(
            email='test0@test.com',
            password='passTeSt123'
        )

        with self.assertRaises(UserAlreadyExistsError):
            await UserProcess.registration(
                email='test0@test.com',
                password='passTeSt1234'
            )

    async def test_registration_check_user(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config.yml')

        await UserProcess.registration(
            email='test1@test.com',
            password='passTeSt123'
        )

        finded_users = await User.find({'email':'test1@test.com'})
        self.assertEqual(len(finded_users), 1)
        self.assertFalse(finded_users[0].check_password('passTeSt1234'))
        self.assertTrue(finded_users[0].check_password('passTeSt123'))

    async def test_registration_check_confirm_token(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config.yml')

        user = await UserProcess.registration(
            email='test2@test.com',
            password='passTeSt123'
        )

        confirm_tokens = await ConfirmToken.find({'user_id': user.object_id})
        self.assertEqual(len(confirm_tokens), 1)

    async def test_registration_check_email(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config.yml')

        user = await UserProcess.registration(
            email='test3@test.com',
            password='passTeSt123'
        )

        emails = await Email.find({'recipient': user.email})
        self.assertEqual(len(emails), 1)

        redis_connection = aioredis.from_url(self.redis_url)
        async with redis_connection.client() as conn:
            redis_data = await conn.get(emails[0].object_id)

        confirm_tokens = await ConfirmToken.find({'user_id': user.object_id})

        rendered_template = await render_template(
            template_root='tests/templates',
            template='confirm_registration.j2',
            data={
                'user': user,
                'confirm_token': confirm_tokens[0],
            }
        )

        message = json.loads(redis_data.decode())
        self.assertEqual(message['message']['subject'], 'Test registration subject')
        self.assertEqual(message['message']['body']['text'], 'Test registration subject')
        self.assertEqual(
            html_to_json.convert(message['message']['body']['html']), 
            html_to_json.convert(rendered_template),
        )

    async def test_registration_check_email_without_confirmation(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config_without_confirmation.yml')

        user = await UserProcess.registration(
            email='test4@test.com',
            password='passTeSt123'
        )

        emails = await Email.find({'recipient': user.email})
        self.assertEqual(len(emails), 1)

        redis_connection = aioredis.from_url(self.redis_url)
        async with redis_connection.client() as conn:
            redis_data = await conn.get(emails[0].object_id)

        rendered_template = await render_template(
            template_root='tests/templates',
            template='success_registration.j2',
            data={
                'user': user,
            }
        )

        message = json.loads(redis_data.decode())
        self.assertEqual(message['message']['subject'], 'Success registration subject')
        self.assertEqual(message['message']['body']['text'], 'Success registration subject')
        self.assertEqual(
            html_to_json.convert(message['message']['body']['html']), 
            html_to_json.convert(rendered_template),
        )

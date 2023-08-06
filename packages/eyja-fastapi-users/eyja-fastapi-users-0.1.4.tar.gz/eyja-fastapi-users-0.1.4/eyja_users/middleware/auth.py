from fastapi import Request

from eyja.utils import load_model

from eyja_users.processes import auth as auth_processes
from eyja_users.operators import (
    RefreshTokenOperator,
    UserOperator,
)
from eyja_users.models import (
    AccessToken,
    RefreshToken,
)


async def auth_middleware(request: Request, call_next):
    refreshed_token = False
    access_token_header = request.headers.get('x-access-token')
    refresh_token_header = request.headers.get('x-refresh-token')

    access_token_model = load_model('users.access_tokens.model', AccessToken)
    refresh_token_model = load_model('users.refresh_tokens.model', RefreshToken)

    if access_token_header:
        access_tokens = await access_token_model.find({
            'token': access_token_header
        })
        access_token = None

        if len(access_tokens) < 1:
            refresh_tokens = await refresh_token_model.find({
                'token': refresh_token_header,
                'status': RefreshTokenOperator.statuses.ACTIVE,
            })

            if len(refresh_tokens) > 0:
                access_token = await auth_processes.RefreshProcess.run(
                    refresh_token=refresh_token_header,
                )
                refreshed_token = True
        else:
            access_token = access_tokens[0]

        if access_token:
            request.scope['current_user'] = await UserOperator.get_user(
                access_token.user_id
            )
            request.scope['access_token'] = access_token

    response = await call_next(request)

    if refreshed_token:
        response.headers["x-new-access-token"] = access_token.token

    return response

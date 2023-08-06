from fastapi import HTTPException, Request

from eyja_users.processes.auth import AuthorizationProcess

from .router import users_router


@users_router.post('/login', name='login_user')
async def login_user(request: Request):
    json_data = await request.json()

    try:
        user, refresh_token, access_token = await AuthorizationProcess.run(**json_data)
    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )

    return {
        'user': user.cleared_data,
        'access_token': access_token.token,
        'refresh_token': refresh_token.token,
    }

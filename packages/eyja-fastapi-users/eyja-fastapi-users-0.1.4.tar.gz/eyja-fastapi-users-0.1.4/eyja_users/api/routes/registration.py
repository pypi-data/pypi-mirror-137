from fastapi import HTTPException, Request

from eyja_users.processes.auth import RegistrationProcess

from .router import users_router


@users_router.post('/registration', name='registration_user')
async def registration_user(request: Request):
    json_data = await request.json()

    try:
        user = await RegistrationProcess.run(**json_data)
    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )

    return {
        'user': user.cleared_data,
    }

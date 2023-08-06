from fastapi import HTTPException, Request

from eyja_users.decorators import login_required

from .router import users_router


@users_router.get('/current', name='current_user')
@login_required
async def current_user(request: Request):
    return {
        'user': request.scope['current_user'].cleared_data,
    }

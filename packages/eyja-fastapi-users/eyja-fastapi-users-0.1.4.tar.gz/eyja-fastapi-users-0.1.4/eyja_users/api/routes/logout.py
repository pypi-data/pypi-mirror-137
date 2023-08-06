from fastapi import HTTPException, Request

from eyja_users.decorators import login_required
from eyja_users.processes.auth import UnauthorizationProcess

from .router import users_router


@users_router.get('/logout', name='logout_user')
@login_required
async def logout_user(request):
    await UnauthorizationProcess.run(
        access_token=request.scope['access_token'],
    )

    return {}

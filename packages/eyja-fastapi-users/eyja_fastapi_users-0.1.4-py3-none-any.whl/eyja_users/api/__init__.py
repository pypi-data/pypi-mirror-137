from fastapi import FastAPI

from .routes.router import users_router


users_api = FastAPI()
users_api.include_router(users_router)

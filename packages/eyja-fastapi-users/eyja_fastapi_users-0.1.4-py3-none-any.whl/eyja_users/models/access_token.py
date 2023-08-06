from eyja.interfaces.db import BaseStorageModel
from eyja.hubs.config_hub import ConfigHub


class AccessToken(BaseStorageModel):
    _namespace = ConfigHub.get('users.access_tokens.namespace', ':::access_tokens')
    _key_template = ConfigHub.get('users.access_tokens.key_template', 'token.refresh_token_id.user_id')
    _expiration = ConfigHub.get('users.access_tokens.expiration', 3*24*60*60)

    token: str
    refresh_token_id: str
    user_id: str

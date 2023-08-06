from eyja.interfaces.db import BaseStorageModel
from eyja.hubs.config_hub import ConfigHub


class RefreshToken(BaseStorageModel):
    _namespace = ConfigHub.get('users.refresh_tokens.namespace', ':::refresh_tokens')
    _key_template = ConfigHub.get('users.refresh_tokens.key_template', 'token.user_id.status')
    _expiration = ConfigHub.get('users.refresh_tokens.expiration', 3*24*60*60)

    token: str
    status: str
    user_id: str

from eyja.interfaces.db import BaseStorageModel
from eyja.hubs.config_hub import ConfigHub


class ConfirmToken(BaseStorageModel):
    _namespace = ConfigHub.get('users.confirm_tokens.namespace', ':::confirm_tokens')
    _key_template = ConfigHub.get('users.confirm_tokens.key_template', 'token.token_type.user_id')
    _expiration = ConfigHub.get('users.confirm_tokens.expiration', 3*24*60*60)

    token: str
    token_type: str
    user_id: str

from eyja.hubs.config_hub import ConfigHub


class AccessTokenConstants:
    TOKEN_LENGTH = ConfigHub.get('users.access_tokens.token_length', 32)
    TOKEN_PREFIX = ConfigHub.get('users.access_tokens.token_prefix', 'at2')

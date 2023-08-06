from eyja.hubs.config_hub import ConfigHub


class ConfirmTokenConstants:
    TOKEN_LENGTH = ConfigHub.get('users.confirm_tokens.token_length', 32)
    TOKEN_PREFIX = ConfigHub.get('users.confirm_tokens.token_prefix', 'ct2')

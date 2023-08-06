from eyja.hubs.config_hub import ConfigHub


class RefreshTokenConstants:
    TOKEN_LENGTH = ConfigHub.get('users.refresh_tokens.token_length', 64)
    TOKEN_PREFIX = ConfigHub.get('users.refresh_tokens.token_prefix', 'rt2')

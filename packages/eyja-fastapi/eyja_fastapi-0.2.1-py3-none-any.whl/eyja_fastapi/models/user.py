from eyja.interfaces.db import BaseStorageModel
from eyja.hubs.config_hub import ConfigHub

from .user_mixin import UserMixin


class User(UserMixin, BaseStorageModel):
    _namespace = ConfigHub.get('users.namespace', ':::users')
    _indexes = [
        'email'
    ] + BaseStorageModel._indexes
    _hidden_fields = [
        'password_hash'
    ]

    email: str


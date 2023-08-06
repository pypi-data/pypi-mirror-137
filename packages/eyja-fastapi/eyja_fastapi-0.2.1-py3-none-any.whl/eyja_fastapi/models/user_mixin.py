from typing import Optional

from pydantic import BaseModel

from passlib.handlers.pbkdf2 import pbkdf2_sha256


class UserMixin(BaseModel):
    password_hash: Optional[str]
    is_active: bool = False
    is_admin: bool = False

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

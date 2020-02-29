from passlib.hash import pbkdf2_sha512
from tortoise import fields

from app.contrib.models import TimestampModel


class User(TimestampModel):
    """
    User model
    """
    id = fields.BigIntField(pk=True)
    login = fields.CharField(max_length=20, unique=True)
    password_hash = fields.CharField(max_length=130, default='')
    first_name = fields.CharField(max_length=50, default='')
    last_name = fields.CharField(max_length=50, default='')
    permissions = fields.JSONField(default=[])
    is_active = fields.BooleanField(default=True)

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def password(self) -> str:
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = pbkdf2_sha512.hash(value)

    def verify(self, password: str) -> bool:
        return pbkdf2_sha512.verify(password, self.password_hash)


class Session(TimestampModel):
    user = fields.ForeignKeyField('models.User', 'sessions')
    refresh_token = fields.UUIDField()
    expired_at = fields.DatetimeField()

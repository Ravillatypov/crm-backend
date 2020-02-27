from tortoise import fields

from app.models.base import TimestampModel


class User(TimestampModel):
    """
    User model
    """
    phone = fields.CharField(unique=True, max_length=15)
    password_hash = fields.CharField(max_length=200, default='')
    first_name = fields.CharField(max_length=50, default='')
    last_name = fields.CharField(max_length=50, default='')
    permissions = fields.JSONField(default=[])
    is_active = fields.BooleanField(default=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

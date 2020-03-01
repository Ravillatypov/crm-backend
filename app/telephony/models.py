from tortoise import fields

from app.contrib.models import TimestampModel


class TelephonySetting(TimestampModel):
    id = fields.BigIntField(pk=True)
    operator = fields.CharField(default='', max_length=15)
    is_active = fields.BooleanField(default=True)
    client_id = fields.CharField(default='', max_length=100, index=True)
    client_key = fields.CharField(default='', max_length=100)
    domain = fields.CharField(default='', max_length=75)
    login = fields.CharField(default='', max_length=20)
    password = fields.CharField(default='', max_length=20)
    days_store_records = fields.SmallIntField(null=True)


class Call(TimestampModel):
    id = fields.UUIDField(pk=True)
    setting = fields.ForeignKeyField('telephony.TelephonySetting')
    session_id = fields.CharField(max_length=50, index=True)
    state = fields.CharField(max_length=20)
    call_type = fields.CharField(max_length=20)
    from_user = fields.CharField(default='', max_length=15)
    from_number = fields.CharField(max_length=15)
    request_user = fields.CharField(default='', max_length=15)
    request_number = fields.CharField(max_length=15)
    started_at = fields.DatetimeField()
    voice_started_at = fields.DatetimeField(null=True)
    voice_finished_at = fields.DatetimeField(null=True)
    finished_at = fields.DatetimeField(null=True)
    is_record = fields.BooleanField(default=False)
    record_url = fields.CharField(max_length=255, null=True)
    uploaded_at = fields.DatetimeField(null=True)

    class Meta:
        ordering = ['started_at']

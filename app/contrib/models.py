from tortoise import models, fields
from tortoise.query_utils import Q


class TimestampModel(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


def get_filter(**kwargs) -> Q:
    return Q(**{k: v for k, v in kwargs.items() if v})

from pydantic import BaseModel


class MessageSchema(BaseModel):
    detail: str = ''


class StatusSchema(BaseModel):
    status: str = 'success'

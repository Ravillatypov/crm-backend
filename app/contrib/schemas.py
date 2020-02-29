from pydantic import BaseModel


class MessageSchema(BaseModel):
    detail: str = ''

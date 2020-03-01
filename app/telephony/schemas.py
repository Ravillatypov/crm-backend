from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel, UUID4


class TelephonySettingSchema(BaseModel):
    id: int
    operator: str
    is_active: bool
    client_id: str
    client_key: str
    domain: str
    login: str
    password: str
    days_store_records: Union[str, None]


class CallSchema(BaseModel):
    id: UUID4
    setting_id: int
    session_id: str
    state: str
    call_type: str
    from_user: str
    from_number: str
    request_number: str
    request_user: str
    started_at: datetime
    voice_started_at: Union[datetime, None]
    voice_finished_at: Union[datetime, None]
    finished_at: Union[datetime, None]
    is_record: bool
    record_url: str
    uploaded_at: Union[datetime, None]


class CallFilterSchema(BaseModel):
    setting_id: Optional[int]
    session_id: Optional[str]
    state: Optional[str]
    call_type: Optional[str]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    is_record: Optional[bool]

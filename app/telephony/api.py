from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends

from app.auth.models import User
from app.contrib.models import get_filter
from app.contrib.utils import jwt_auth, check_permissions
from app.telephony.models import Call
from app.telephony.schemas import CallSchema

v1 = APIRouter()


@v1.get('/calls', response_model=List[CallSchema], tags=['telephony'])
async def get_calls(
        user: User = Depends(jwt_auth),
        offset: int = 0,
        limit: int = 100,
        setting_id: Optional[int] = None,
        session_id: Optional[str] = None,
        state: Optional[str] = None,
        call_type: Optional[str] = None,
        started_at: Optional[datetime] = None,
        finished_at: Optional[datetime] = None,
        is_record: Optional[bool] = None,
        ordering: Optional[List[str]] = None,
):
    order_keys = ('started_at', 'is_record', 'state', 'call_type')
    check_permissions(user, 'calls')
    filters = get_filter(
        setting_id=setting_id,
        session_id=session_id,
        state=state,
        call_type=call_type,
        started_at=started_at,
        finished_at=finished_at,
        is_record=is_record,
    )
    qs = Call.filter(filters)
    if offset:
        qs = qs.offset(offset)
    qs = qs.limit(limit)
    if ordering:
        order_by = [key for key in ordering if key in order_keys]
        if order_by:
            qs = qs.order_by(*order_by)
    return await qs

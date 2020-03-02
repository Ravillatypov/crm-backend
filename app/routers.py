from app.auth.api import v1 as auth_v1
from app.telephony.api import v1 as telephony_v1

# prefix, router
routes = [
    ('/api/v1/auth', auth_v1),
    ('/api/v1/telephony', telephony_v1),
]

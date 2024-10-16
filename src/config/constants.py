from sqlalchemy import Enum

API_V1 = "/api/v1"
API = API_V1
AUTH = "/auth"
ACCOUNTS = "/accounts"

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 255
MAX_NOTE_LENGTH = 500
MAX_ACTIVE_SESSIONS = 5

TRANSACTION_TYPE_ENUM = Enum(
    "INVESTMENT",
    "WITHDRAW",
    name="transaction_type_enum",
)

EMAIL_TOKEN_HOURS_TO_EXPIRE = 24

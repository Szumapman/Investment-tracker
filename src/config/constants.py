from sqlalchemy import Enum

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 255
MAX_NOTE_LENGTH = 500

TRANSACTION_TYPE_ENUM = Enum(
    "INVESTMENT",
    "WITHDRAW",
    name="transaction_type_enum",
)

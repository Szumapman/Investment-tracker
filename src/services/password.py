import bcrypt

from src.services.abstract import AbstractPasswordHandler


class BcryptPasswordHandler(AbstractPasswordHandler):
    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

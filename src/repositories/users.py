from sqlalchemy.orm import Session

from src.repositories.abstract import AbstractUserRepo
from src.database.models import User
from src.schemas.users import UserIn


class PostgresUserRepo(AbstractUserRepo):
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    async def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    async def create_user(self, user: UserIn) -> User:
        new_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    async def confirm_user_email(self, email: str) -> User:
        user = await self.get_user_by_email(email)
        if user:
            user.is_confirmed = True
            self.db.commit()
            self.db.refresh(user)
        return user

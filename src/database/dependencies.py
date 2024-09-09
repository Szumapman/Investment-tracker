from src.database.db import get_db
from src.repositories.abstract import AbstractUserRepo
from src.repositories.users import PostgresUserRepo


def get_user_repo() -> AbstractUserRepo:
    return PostgresUserRepo(next(get_db()))

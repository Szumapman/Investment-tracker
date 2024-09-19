from datetime import datetime, timezone

from src.repositories.abstract import AbstractTokenRepo
from src.database.models import RefreshToken
from src.config.constants import MAX_ACTIVE_SESSIONS


class PostgresTokenRepo(AbstractTokenRepo):
    def __init__(self, db):
        self.db = db

    async def add_refresh_token(
        self, refresh_token: str, user_id: int, session_id: str, expires_at: datetime
    ) -> bool:
        await self.remove_expired_refresh_tokens(user_id)
        user_logged_sessions = (
            self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).all()
        )
        if (
            len(user_logged_sessions) >= MAX_ACTIVE_SESSIONS
        ):  # user can have limited number of sessions
            return False
        new_refresh_token = RefreshToken(
            token=refresh_token,
            user_id=user_id,
            session_id=session_id,
            expires_at=expires_at,
        )
        self.db.add(new_refresh_token)
        self.db.commit()
        return True

    async def get_refresh_token(self, refresh_token: str) -> RefreshToken | None:
        return (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token == refresh_token)
            .first()
        )

    async def remove_expired_refresh_tokens(self, user_id: int) -> None:
        self.db.query(RefreshToken).filter(
            RefreshToken.expires_at < datetime.now(timezone.utc)
        ).delete()

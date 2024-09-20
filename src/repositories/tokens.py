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
        ):  # because user can have limited number of sessions
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

    async def delete_refresh_token(
        self, refresh_token: str = None, user_id: int = None, session_id: str = None
    ) -> None:
        if refresh_token:
            self.db.query(RefreshToken).filter(
                RefreshToken.token == refresh_token
            ).delete()
        elif user_id and session_id:
            self.db.query(RefreshToken).filter(
                RefreshToken.user_id == user_id, RefreshToken.session_id == session_id
            ).delete()
        else:
            raise ValueError(
                "Either refresh_token or user_id and session_id must be provided"
            )
        self.db.commit()
        await self.remove_expired_refresh_tokens(user_id)

    async def remove_expired_refresh_tokens(self, user_id: int) -> None:
        self.db.query(RefreshToken).filter(
            RefreshToken.expires_at < datetime.now(timezone.utc)
        ).delete()

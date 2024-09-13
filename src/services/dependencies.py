from src.services.abstract import (
    AbstractPasswordHandler,
    AbstractEmailService,
)
from src.services.password import BcryptPasswordHandler
from src.services.email import FastApiEmailService


def get_password_handler() -> AbstractPasswordHandler:
    return BcryptPasswordHandler()


def get_email_handler() -> AbstractEmailService:
    return FastApiEmailService()

from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.abstract import AbstractEmailService
from src.services.auth import auth_service
from src.config.config import settings
from src.config.constants import API


class FastApiEmailService(AbstractEmailService):
    """
    Service for sending emails.
    """

    EMAIL_CONFIRMATION_BASE_LINK_PART = f"{API}/auth/confirmed_email/"

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_FROM=settings.mail_from,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_FROM_NAME=settings.mail_from_name,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False,
        TEMPLATE_FOLDER=Path(__file__).parent / "templates",
    )

    async def send_confirmation_email(
        self, email: str, username: str, host: str
    ) -> None:
        """
        Sends email to the provided email address

        Args:
            email (str): email address to send email
            username (str): username to be displayed in the email
            host (str): host to be displayed in the confirmation link in the email
        """
        try:
            token_verification = auth_service.create_email_token({"sub": email})
            message = MessageSchema(
                subject="Confirm your email ",
                recipients=[email],
                template_body={
                    "username": username,
                    "email_confirmaton_link": f"{host}{self.EMAIL_CONFIRMATION_BASE_LINK_PART}{token_verification}",
                },
                subtype=MessageType.html,
            )
            fast_mail = FastMail(self.conf)
            await fast_mail.send_message(message, template_name="email_template.html")
        except ConnectionErrors as err:
            print(err)  # ToDo: add log

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Args:
        model_congig  (SettingsConfigDict): Configuration for the pydantic-settings.
        database_name (str): Name of the database.
        database_username (str): Username for the database.
        database_password (str): Password for the database.
        database_host (str): Hostname of the database.
        database_port (str): Port number of the database.
        sqlalchemy_database_url (str): URL for the SQLAlchemy database.
        secret_key (str): Secret key for the application encryption.
        algorithm (str): Algorithm for the application encryption.
        access_token_expire_minutes (int): Expiration time for access tokens in minutes.
        refresh_token_expire_days (int): Expiration time for refresh tokens in days.
        redis_host (str): Hostname of the Redis server.
        redis_port (str): Port number of the Redis server.
        redis_password (str): Password for the Redis server.
        mail_username (str): Username for the email server.
        mail_password (str): Password for the email server.
        mail_from (str): Email address for the sender.
        mail_port (int): SMTP port number of the email server.
        mail_server (str): SMTP server hostname of the email server.
        mail_from_name (str): Name of the sender.
        mail_starttls (bool): Whether to use STARTTLS for the email server.
        mail_ssl_tls (bool): Whether to use SSL/TLS for the email server.
        validate_certs (bool): Whether to validate SSL/TLS certificates for the email server.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_name: str
    database_username: str
    database_password: str
    database_host: str
    database_port: str
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    redis_host: str
    redis_port: str
    redis_password: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str
    mail_starttls: bool
    mail_ssl_tls: bool
    validate_certs: bool


settings = Settings()

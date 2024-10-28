from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    func,
    JSON,
)
from sqlalchemy.orm import relationship, declarative_base

from src.config.constants import (
    MAX_USERNAME_LENGTH,
    TRANSACTION_TYPE_ENUM,
    MAX_NOTE_LENGTH,
)

Base = declarative_base()


class User(Base):
    """
    Model for the users table.

    Attributes:
        id (int): primary key
        username (str): username of the user
        email (str): email of the user
        password (str): user password
        created_at (DateTime): date and time when the user was created
        updated_at (DateTime): date and time when the user was last updated
        is_active (bool): whether the user is active

        accounts (relationship): relationship with the accounts table
        refresh_tokens (relationship): relationship with the refresh_tokens table
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(MAX_USERNAME_LENGTH), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_confirmed = Column(Boolean, default=False)

    accounts = relationship("Account", backref="user", cascade="all, delete-orphan")
    refresh_tokens = relationship(
        "RefreshToken", backref="user", cascade="all, delete-orphan"
    )


class Account(Base):
    """
    Model for the accounts table.

    Attributes:
        id (int): primary key
        user_id (int): foreign key to the users table
        balance_investable_funds (float): balance of money available for investment
        currency (str): currency of the account
        created_at (DateTime): date and time when the account was created

        transactions (relationship): relationship with the transactions table
    """

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    balance_investable_funds = Column(Float, default=0.00)
    currency = Column(String(3), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship(
        "Transaction", backref="account", cascade="all, delete-orphan"
    )


class Transaction(Base):
    """
    Model for the transactions table.

    Attributes:
        id (int): primary key
        account_id (int): foreign key to the accounts table
        deposit_id (int): foreign key to the deposits table
        asset_id (int): foreign key to the assets table
        currency_invest_id (int): foreign key to the currency_invests table
        type (TRANSACTION_TYPE_ENUM): type of the transaction
        amount (float): amount of the transaction in the account's currency
        note (str): note to the transaction
        created_at (DateTime): date and time when the transaction was created
    """

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    deposit_id = Column(Integer, ForeignKey("deposits.id", ondelete="CASCADE"))
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"))
    currency_invest_id = Column(
        Integer, ForeignKey("currency_invests.id", ondelete="CASCADE")
    )
    type = Column(TRANSACTION_TYPE_ENUM, nullable=False)
    amount = Column(Float, nullable=False)
    note = Column(String(MAX_NOTE_LENGTH))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Deposit(Base):
    """
    Model for the deposits table.

    Attributes:
        id (int): primary key
        account_id (int): foreign key to the accounts table
        amount (float): amount of the deposit
        interest_rate (float): interest rate of the deposit
        maturity_date (DateTime): maturity date of the deposit
    """

    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    maturity_date = Column(DateTime(timezone=True), nullable=False)

    transactions = relationship(
        "Transaction", backref="deposit", cascade="all, delete-orphan"
    )


class Asset(Base):
    """
    Model for the assets table.

    Attributes:
        id (int): primary key
        account_id (int): foreign key to the accounts table
        purchase_amount (float): amount of the purchase
        purchase_date (DateTime): date and time when the asset was purchased
        purchase_share_price (float): purchase share price of the asset
        share_quantity (float): quantity of shares of the asset
        current_share_quantity (float): current quantity of shares of the asset

        transactions (relationship): relationship with the transactions table
    """

    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    asset_name = Column(String(10), nullable=False)
    purchase_amount = Column(Float, nullable=False)
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())
    purchase_share_price = Column(Float, nullable=False)
    share_quantity = Column(Float, nullable=False)
    current_share_quantity = Column(Float, nullable=False)

    transactions = relationship(
        "Transaction", backref="asset", cascade="all, delete-orphan"
    )


class CurrencyInvest(Base):
    """
    Model for the currency_invests table.

    Attributes:
        id (int): primary key
        account_id (int): foreign key to the accounts table
        purchase_amount (float): amount of the purchase in the currency of the investment
        currency (str): currency of the investment
        purchase_exchange_rate (float): exchange rate of the purchase
        purchase_date (DateTime): date and time when the investment was purchased
        current_amount (float): current amount of the investment in the currency of the investment

        transactions (relationship): relationship with the transactions table
    """

    __tablename__ = "currency_invests"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )

    purchase_amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    purchase_exchange_rate = Column(Float, nullable=False)
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())
    current_amount = Column(Float, nullable=False)

    transactions = relationship(
        "Transaction", backref="currency_invest", cascade="all, delete-orphan"
    )


class RefreshToken(Base):
    """
    Model for the refresh_tokens table.

    Attributes:
        id (int): primary key
        user_id (int): foreign key to the users table
        token (str): refresh token
        session_id (JSON): session id
        expires_at (DateTime): expiration date of the refresh token
    """

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token = Column(String(350), nullable=False)
    session_id = Column(String(350), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

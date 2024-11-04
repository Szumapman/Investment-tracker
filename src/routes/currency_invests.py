from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config.constants import CURRENCIES
from src.schemas.currency_invests import (
    CurrencyInvestIn,
    CurrencyInvestToBuy,
    CurrencyInvestOut,
    CurrencyInvestInfo,
)
from src.schemas.transactions import TransactionIn
from src.services.auth import auth_service
from src.database.models import User, Account
from src.repositories.abstract import AbstractAccountRepo, AbstractCurrencyInvestRepo
from src.database.dependencies import get_account_repo, get_currency_invest_repo

router = APIRouter(prefix=CURRENCIES, tags=["currencies"])


async def __get_account(account_id: int, account_repo: AbstractAccountRepo) -> Account:
    account = await account_repo.get_account_by_id(account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    return account


async def __check_authorization(account_user_id: int, current_user_id: int) -> None:
    if account_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )


@router.post(
    "/",
    response_model=CurrencyInvestInfo,
    status_code=status.HTTP_201_CREATED,
)
async def create_currency_invest(
    transaction_in: TransactionIn,
    currency_invest: CurrencyInvestIn,
    current_user: User = Depends(auth_service.get_current_user),
    account_repo: AbstractAccountRepo = Depends(get_account_repo),
    currency_invest_repo: AbstractCurrencyInvestRepo = Depends(
        get_currency_invest_repo
    ),
) -> CurrencyInvestInfo:
    account = await __get_account(transaction_in.account_id, account_repo)
    await __check_authorization(account.user_id, current_user.id)
    if account.balance_investable_funds < transaction_in.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds",
        )
    currency_invest_to_buy = CurrencyInvestToBuy(
        currency=currency_invest.currency,
        purchase_exchange_rate=2,
    )
    new_currency_invest = await currency_invest_repo.create_currency_invest(
        transaction_in, currency_invest_to_buy
    )
    return CurrencyInvestInfo(
        currency_invest=CurrencyInvestOut.model_validate(new_currency_invest),
        detail="Currency invest created successfully",
    )

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config.constants import ACCOUNTS
from src.schemas.accounts import AccountIn, AccountOut, AccountInfo, AccountFunds
from src.database.models import User, Account
from src.services.auth import auth_service
from src.repositories.abstract import AbstractAccountRepo
from src.database.dependencies import get_account_repo


router = APIRouter(prefix=ACCOUNTS, tags=["accounts"])

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

@router.post("/", response_model=AccountInfo, status_code=status.HTTP_201_CREATED)
async def create_account(account_info: AccountIn, current_user: User = Depends(auth_service.get_current_user), account_repo: AbstractAccountRepo = Depends(get_account_repo)) -> AccountInfo:
    accounts = await account_repo.get_accounts(current_user.id)
    if accounts is not None:
        for account in accounts:
            if account.currency == account_info.currency:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Account with this currency already exists",
                )
    new_account = await account_repo.create_account(current_user.id, account_info)
    return AccountInfo(account=AccountOut.model_validate(new_account), detail="Account created successfully")

@router.post("/{account_id}/deposit", response_model=AccountInfo)
async def deposit_funds(amount_funds: AccountFunds, account_id: int, current_user: User = Depends(auth_service.get_current_user), account_repo: AbstractAccountRepo = Depends(get_account_repo)) -> AccountInfo:
    account = await __get_account(account_id, account_repo)
    __check_authorization(account.user_id, current_user.id)
    account = await account_repo.update_funds(account_id, amount_funds.balance_investable_funds)
    return AccountInfo(account=AccountOut.model_validate(account), detail=f"Added funds in the amount of {amount_funds.balance_investable_funds} {account.currency} to the account")
                
@router.post("/{account_id}/withdraw", response_model=AccountInfo)
async def withdraw_funds(amount_funds: AccountFunds, account_id: int, current_user: User = Depends(auth_service.get_current_user), account_repo: AbstractAccountRepo = Depends(get_account_repo)) -> AccountInfo:
    account = await __get_account(account_id, account_repo)
    __check_authorization(account.user_id, current_user.id)
    if  account.balance_investable_funds < amount_funds.balance_investable_funds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds",
        )
    account = await account_repo.update_funds(account_id, -amount_funds.balance_investable_funds)
    return AccountInfo(account=AccountOut.model_validate(account), detail=f"Withdrawn funds in the amount of {amount_funds.balance_investable_funds} {account.currency} from the account")
    
@router.delete("/{account_id}", response_model=AccountInfo)
async def delete_account(account_id: int, current_user: User = Depends(auth_service.get_current_user), account_repo: AbstractAccountRepo = Depends(get_account_repo)) -> AccountInfo:
    account = await __get_account(account_id, account_repo)
    __check_authorization(account.user_id, current_user.id)
    if account.balance_investable_funds != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account has funds, please withdraw them before deleting the account",
        )
    account = await account_repo.delete_account(account_id)
    return AccountInfo(account=AccountOut.model_validate(account), detail="Account deleted successfully")
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config.constants import ACCOUNTS
from src.schemas.accounts import AccountIn, AccountOut, AccountInfo
from src.database.models import User
from src.services.auth import auth_service
from src.repositories.abstract import AbstractAccountRepo
from src.database.dependencies import get_account_repo


router = APIRouter(prefix=ACCOUNTS, tags=["accounts"])

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

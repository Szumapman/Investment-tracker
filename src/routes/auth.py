from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Security,
    Depends,
    BackgroundTasks,
    Request,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from src.repositories.abstract import AbstractUserRepo
from src.database.dependencies import get_user_repo
from src.services.dependencies import get_password_handler, get_email_handler
from src.schemas.users import UserIn, UserOut, UserInfo
from src.schemas.tokens import TokenOut
from src.config.constants import AUTH

router = APIRouter(prefix=AUTH, tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def signup(
    user: UserIn,
    background_tasks: BackgroundTasks,
    request: Request,
    email_service=Depends(get_email_handler),
    user_repo: AbstractUserRepo = Depends(get_user_repo),
    password_handler=Depends(get_password_handler),
) -> UserInfo:
    if await user_repo.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    if await user_repo.get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )
    user.password = await password_handler.hash_password(user.password)
    print(len(user.password))
    user = await user_repo.create_user(user)
    background_tasks.add_task(
        email_service.send_confirmation_email,
        user.email,
        user.username,
        request.base_url,
    )
    return UserInfo(
        user=UserOut.model_validate(user),
        detail="User created successfully, please check your email to verify your account",
    )

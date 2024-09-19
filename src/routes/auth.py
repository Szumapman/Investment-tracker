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

from src.repositories.abstract import AbstractUserRepo, AbstractTokenRepo
from src.database.dependencies import get_user_repo, get_token_repo
from src.services.dependencies import get_password_handler, get_email_handler
from src.services.auth import auth_service
from src.schemas.users import UserIn, UserOut, UserInfo, ResetPassword
from src.schemas.email import RequestEmail
from src.schemas.tokens import TokenOut
from src.config.constants import AUTH, MAX_ACTIVE_SESSIONS

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
    user.password = await password_handler.hash_password(user.password.password)
    user = await user_repo.create_user(user)
    background_tasks.add_task(
        email_service.send_email,
        "confirm",
        user.email,
        user.username,
        request.base_url,
    )
    return UserInfo(
        user=UserOut.model_validate(user),
        detail="User created successfully, please check your email to verify your account",
    )


@router.get("/confirmed_email/{token}")
async def confirmed_email(
    token: str,
    user_repo: AbstractUserRepo = Depends(get_user_repo),
) -> dict[str, str]:
    email = await auth_service.get_email_from_token(token)
    user = await user_repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification error",
        )
    if user.is_confirmed:
        return {"message": "Your email is already confirmed"}
    await user_repo.confirm_user_email(email)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    user_repo: AbstractUserRepo = Depends(get_user_repo),
    email_service=Depends(get_email_handler),
) -> dict[str, str]:
    user = await user_repo.get_user_by_email(body.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification error",
        )
    if user.is_confirmed:
        return {"message": "Your email is already confirmed"}
    background_tasks.add_task(
        email_service.send_email,
        body.request_type,
        user.email,
        user.username,
        request.base_url,
    )
    return {"message": "Check your email for confirmation."}


@router.post("/request_password_reset")
async def request_password_reset(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    user_repo: AbstractUserRepo = Depends(get_user_repo),
    email_service=Depends(get_email_handler),
) -> dict[str, str]:
    user = await user_repo.get_user_by_email(body.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification error",
        )
    background_tasks.add_task(
        email_service.send_email,
        body.request_type,
        user.email,
        user.username,
        request.base_url,
    )
    return {"message": "Check your email for a link to reset your password."}


@router.post("/reset_password/{token}")
async def reset_password(
    token: str,
    body: ResetPassword,
    user_repo: AbstractUserRepo = Depends(get_user_repo),
    password_handler=Depends(get_password_handler),
) -> UserInfo:
    email = await auth_service.get_email_from_token(token)
    user = await user_repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification error",
        )
    user.password = await password_handler.hash_password(body.password.password)
    user = await user_repo.update_password(user)
    return UserInfo(
        user=UserOut.model_validate(user), detail="Password updated successfully"
    )


@router.post("/login", response_model=TokenOut)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: AbstractUserRepo = Depends(get_user_repo),
    token_repo: AbstractTokenRepo = Depends(get_token_repo),
    password_handler=Depends(get_password_handler),
) -> TokenOut:
    user = await user_repo.get_user_by_email(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
        )
    if not await password_handler.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token, session_id = await auth_service.create_access_token(
        data={"sub": user.email}
    )
    refresh_token, expire = await auth_service.create_refresh_token(
        data={"sub": user.email}
    )
    if not await token_repo.add_refresh_token(
        refresh_token, user.id, session_id, expire
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Too many active sessions. User must not have more than {MAX_ACTIVE_SESSIONS} active sessions",
        )
    return TokenOut(
        access_token=access_token,
        refresh_token=refresh_token,
    )

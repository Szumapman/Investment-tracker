from pydantic import BaseModel


class TokenOut(BaseModel):
    """
    Schema for the token response

    Attributes:
        access_token (str): access token for the user
        refresh_token (str): refresh token for the user
        token_type (str): type of the token
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"

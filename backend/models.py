from pydantic import BaseModel


class UserForm(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name : str | None = None
    disabled : bool | None = None
    aadhaar : int | None = None
    day : int | None = None
    month : int | None = None
    year : int | None = None
    wallet : str | None = None
    password : str | None = None
    private_key : str | None = None


class UserData(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None
    aadhaar: int | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
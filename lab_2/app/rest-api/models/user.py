from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: int
    user_name: str
    first_name: str
    second_name: str
    password: str


class UpdateUserModel(BaseModel):
    user_name: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    password: str | None = None

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str


class UserGetSchema(UserBaseSchema):
    id: int

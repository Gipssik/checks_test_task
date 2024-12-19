from pydantic import BaseModel


class OKResponse(BaseModel):
    OK: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str

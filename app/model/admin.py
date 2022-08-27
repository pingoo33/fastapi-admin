from pydantic import BaseModel


class AdminSignInRequestDto(BaseModel):
    email: str
    password: str

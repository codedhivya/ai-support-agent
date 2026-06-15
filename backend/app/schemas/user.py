from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginForm(BaseModel):
    username: EmailStr
    password: str

class RegisterInput(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

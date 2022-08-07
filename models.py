from pydantic import BaseModel, Field


class Personal(BaseModel):
    first_name: str = Field(title='First name')
    last_name: str = Field(title='Last name')
    email: str = Field(title='Email')


class UserDetails(Personal):
    group: str = Field(title='Group')


class SignUpRequest(Personal):
    password: str = Field(title='Password')
    group_id: int = Field(title="Group ID")
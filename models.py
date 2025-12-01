from pydantic import BaseModel ,  Field, ConfigDict, EmailStr
from typing import Optional

class NotesModel(BaseModel):
    id : int = Field(...)
    heading: str = Field(..., min_length=5)
    pointers : str = Field(...)

    model_config = ConfigDict(from_attributes=True)


class NotesDisplayModel(BaseModel):
    heading: str = Field(..., min_length=5)
    pointers : str = Field(...)

    model_config = ConfigDict(from_attributes=True)

class NotesUpdateModel(BaseModel):
    heading : Optional[str] = None
    pointers : Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserInDB(UserBase):
    id: int
    hashed_password: str
    disabled: bool = False

    model_config = ConfigDict(from_attributes=True)

class UserPublic(UserBase):
    id: int
    disabled: bool = False

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

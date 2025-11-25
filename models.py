from pydantic import BaseModel ,  Field, ConfigDict
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



from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """
    pass


class IDModelMixin(BaseModel):
    id: int


class DateTimeModelMixin(BaseModel):
    created_at: Optional[str]
    updated_at: Optional[str]

    @validator('created_at', 'updated_at', pre=True)
    def default_datetime(cls, v):
        return v or datetime.datetime.now()

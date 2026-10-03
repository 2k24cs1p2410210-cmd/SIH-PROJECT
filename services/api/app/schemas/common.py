from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: Optional[str] = None
    data: Optional[T] = None
    timestamp: datetime


class ErrorResponse(BaseModel):
    status: str = "error"
    detail: str
    code: Optional[str] = None
    timestamp: datetime

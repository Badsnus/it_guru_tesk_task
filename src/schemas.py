from pydantic import BaseModel


class RateSchema(BaseModel):
    rate: float


class ExceptionSchema(BaseModel):
    error: str

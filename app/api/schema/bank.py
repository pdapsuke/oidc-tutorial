from pydantic import BaseModel

class BankGetSchema(BaseModel):
    id: int
    bank_name: str

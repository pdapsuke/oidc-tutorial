from datetime import datetime

from pydantic import BaseModel

from models import AccountType

class BankResponseSchema(BaseModel):
    id: int
    bank_name: str

    class Config:
        orm_mode = True


class BranchResponseSchema(BaseModel):
    id: int
    bank_id: int
    branch_name: str


class AccountInfoResponseSchema(BaseModel):
    id: int
    user_id: int
    bank_name: str
    branch_name: str
    account_type: AccountType
    account_number: str
    secret_number: str
    created: datetime

    class Config:
        orm_mode = True


class AccountInfoCreateSchema(BaseModel):
    branch_id: int
    user_id: int
    account_type: AccountType
    account_number: str
    secret_number: str
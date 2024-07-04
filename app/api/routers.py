from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Bank
from schema.bank import BankGetSchema
from session import get_session

router = APIRouter()

@router.get("/banks/", response_model=List[BankGetSchema])
def get_banks(session: Session = Depends(get_session)):
    banks = session.query(Bank).all()
    return banks

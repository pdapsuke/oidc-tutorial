from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import auth
from models import AccountInfo, Bank, Branch, User
from schema import AccountInfoCreateSchema, AccountInfoResponseSchema, BankResponseSchema, BranchResponseSchema
from session import get_session

router = APIRouter()

@router.get("/login/")
def login(_: User = Depends(auth.get_user_by_token)):
    return JSONResponse(status_code=200, content={"message": "login success!"})

@router.get("/banks/", response_model=List[BankResponseSchema])
def get_banks(session: Session = Depends(get_session)):
    banks = session.query(Bank).all()
    return banks

@router.get("/branches/", response_model=List[BranchResponseSchema])
def get_branches(session: Session = Depends(get_session)):
    branches = session.query(Branch).all()
    return branches

@router.get("/account_infos/", response_model=List[AccountInfoResponseSchema])
def get_account_infos(
    user: User = Depends(auth.get_user_by_token),
    session: Session = Depends(get_session),
):
    account_infos: List[AccountInfo] = session.query(AccountInfo).filter(AccountInfo.user_id == user.id)
    response: List[AccountInfoResponseSchema] = []

    for ai in account_infos:
        branch = session.query(Branch).filter(Branch.id == ai.branch_id).first()
        branch_name: str = branch.branch_name
        bank_name: str = session.query(Bank).filter(Bank.id == branch.bank_id).first().bank_name
        ai.branch_name = branch_name
        ai.bank_name = bank_name
        response.append(ai)

    return response

@router.post("/account_infos/")
def create_account_info(
    data: AccountInfoCreateSchema,
    user: User = Depends(auth.get_user_by_token),
    session: Session = Depends(get_session)
):
    branch = session.query(Branch).filter(Branch.id == data.branch_id).first()
    if branch is None:
        raise HTTPException(status_code=400, detail="branch not exists")

    if len(data.account_number) != 7:
        raise HTTPException(status_code=400, detail="account_number must be 7 digits")

    if len(data.secret_number) != 4:
        raise HTTPException(status_code=400, detail="secret_number must be 4 digits")

    # 既に口座情報が存在する場合はエラーを返す
    existing_account_info = session.query(AccountInfo) \
        .filter(AccountInfo.user_id == user.id) \
        .filter(AccountInfo.branch_id == data.branch_id) \
        .filter(AccountInfo.account_type == data.account_type) \
        .filter(AccountInfo.account_number == data.account_number).first()

    if existing_account_info:
        raise HTTPException(status_code=400, detail="already registerd account info")

    account_info = AccountInfo(
        branch_id = data.branch_id,
        user_id = user.id,
        account_type = data.account_type,
        account_number = data.account_number,
        secret_number = data.secret_number,
    )

    session.add(account_info)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "account_info created"})

@router.delete("/account_infos/{id}")
def delete_account_info(
    id: int,
    user: User = Depends(auth.get_user_by_token),
    session: Session = Depends(get_session),
):
    account_info = session.query(AccountInfo).filter(AccountInfo.id == id).first()
    if account_info is None:
        raise HTTPException(status_code=400, detail="account_info not exists")

    if account_info.user_id != user.id:
        raise HTTPException(status_code=400, detail="you can delete your own account_info")

    session.delete(account_info)
    session.commit()
    return JSONResponse(status_code=200, content={"message": f"account_info(user_id={account_info.id} deleted)"})

###############################################
##             デバッグ用に実装               ##
###############################################
@router.get("/users/")
def get_users(
    session: Session = Depends(get_session),
):
    users = session.query(User).all()
    return users

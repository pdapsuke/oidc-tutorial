from datetime import datetime
import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey

# モデルのベースクラスを定義
from sqlalchemy.orm.decl_api import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255, collation="utf8mb4_bin"), nullable=False)
    email = Column(String(255, collation="utf8mb4_bin"), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # account_infosテーブルとの一対多のリレーション
    account_infos = relationship(
        "AccountInfo",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class AccountType(enum.Enum):
    normal = "普通口座"
    term = "定期口座"
    general = "総合口座"


class AccountInfo(Base):
    __tablename__ = "account_infos"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    account_number = Column(String(7, collation="utf8mb4_bin"), nullable=False)
    secret_number = Column(String(4, collation="utf8mb4_bin"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # branchesテーブルとの多対一のリレーション
    branch = relationship(
        "Branch",
        back_populates="account_infos",
    )

    # usersテーブルとの多対一のリレーション
    user = relationship(
        "User",
        back_populates="account_infos",
    )


class Bank(Base):
    __tablename__ = "banks"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String(255, collation="utf8mb4_bin"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # branchesテーブルとの一対多のリレーション
    branches = relationship(
        "Branch",
        back_populates="bank",
    )


class Branch(Base):
    __tablename__ = "branches"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    branch_name = Column(String(255, collation="utf8mb4_bin"), nullable=False)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # banksテーブルとの多対一のリレーション
    bank = relationship(
        "Bank",
        back_populates="branches",
    )

    # account_infosテーブルとの一対多のリレーション
    account_infos = relationship(
        "AccountInfo",
        back_populates="branch",
    )

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from env import Environment

env = Environment()
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{env.db_user}:{env.db_password}@{env.db_host}:{env.db_port}/{env.db_name}?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = True, bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

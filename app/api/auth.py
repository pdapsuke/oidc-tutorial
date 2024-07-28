from typing import Annotated
import json

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jwt.algorithms import RSAAlgorithm
import requests
import jwt

from models import User
from session import get_session

security = HTTPBearer()

def verify_token(token:str) -> dict:
    issuer_url = "http://localhost:8888/realms/oidc-tutorial"
    jwk_url = "http://localhost:8888/realms/oidc-tutorial/protocol/openid-connect/certs"

    try:
        # tokenのヘッダからKeyIDと署名アルゴリズムを取得
        jwt_header = jwt.get_unverified_header(token)
        key_id = jwt_header["kid"]
        jwt_algorithms = jwt_header["alg"]

        # jwk_urlから公開鍵を取得
        jwk_url_res = requests.get(jwk_url)
        jwk = None
        for key in json.loads(jwk_url_res.text)["keys"]:
            if key["kid"] == key_id:
                jwk = key
        if not jwk:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "token invalid"})
        public_key = RSAAlgorithm.from_jwk(json.dumps(jwk))

        # トークンデコード（検証）
        json_payload = jwt.decode(
            token,
            public_key,
            algorithms=[jwt_algorithms],
            verify=True,
            audience = "account",
            options={"require_exp": True},
            issuer=issuer_url,
        )
        return json_payload

    except:
        raise Exception

def get_user_by_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials

    json_payload = verify_token(token)

    # userオブジェクトの取得
    user = session.query(User).filter(User.email==json_payload["email"]).first()

    # userが未作成の場合は新規作成
    if user is None:
        user = User(
            user_name = json_payload["name"],
            email = json_payload["email"]
        )
        session.add(user)
        session.commit()
        return user
    return user

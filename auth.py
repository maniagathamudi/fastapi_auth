from datetime import datetime, timedelta
import requests
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from settings import settings


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


security = HTTPBearer()

jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
jwks = requests.get(jwks_url).json()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    # ---------------------
    # 1️⃣ Try Local JWT
    # ---------------------
    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except JWTError:
        pass

    # ---------------------
    # 2️⃣ Try Auth0 Token
    # ---------------------
    try:

        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == unverified_header.get("kid"):
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

        if rsa_key == {}:
            raise HTTPException(status_code=401, detail="Invalid token")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.AUTH0_CLIENT_ID,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )

        return payload

    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta
from jose import jwt, JWTError

from schema import TokenData

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

KVUri = f"https://ptt-app-stage.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

JWT_SECRET_KEY = client.get_secret('JWT-SECRET-KEY').value

SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#, current_user: UserInfo = Depends(get_current_user)
async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None: raise credentials_exception

        token_data = TokenData(
            user_id=payload.get("user_id"),
            username=payload.get("username"),
            email=payload.get("email"),
            company=payload.get("company"),
            place=payload.get("place"),
            phone=payload.get("phone")
            )

    except JWTError:
        raise credentials_exception

    return token_data
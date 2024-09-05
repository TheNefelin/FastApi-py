from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import os
from app.mssql import execute_sp

TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")
TOKEN_TIMEOUT = int(os.getenv("TOKEN_TIMEOUT"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

class sp_result(BaseModel):
  code: int
  msge: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data: dict):
  to_encode = data.copy()

  expires_delta = timedelta(minutes = TOKEN_TIMEOUT)

  if expires_delta:
    expire = datetime.now().astimezone() + expires_delta
  else:
    expire = datetime.now().astimezone() + timedelta(minutes = 15)
  
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm = TOKEN_ALGORITHM)
  return encoded_jwt

# Function to verify the token and extract user information
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
  result = await execute_sp("PY_Login", (form_data.username, form_data.password,))
  code, msge = result[0]['StatusCode'], result[0]['Msge']

  if code != 201:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = msge,
      headers = {"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token(data={"sub": form_data.username})

  return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  token_data = verify_token(token, credentials_exception)
  return {"username": token_data.username}
from typing import Annotated
from fastapi import Depends, FastAPI,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from routers import authToken
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    return authToken.verify_token(token,credentials_exception)
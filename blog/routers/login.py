from fastapi import APIRouter,HTTPException,status,Depends
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
import schemas
from database import conn
from hashing import Hash
from . import authToken
router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)
@router.post('/')
#pip install python-multipart for jwt token authentication
def authentication(request:OAuth2PasswordRequestForm=Depends()):
    cursor = conn.cursor(buffered=True)
    user = f"SELECT * FROM user where email = '{request.username}'"
    
    cursor.execute(user)
    conn.commit()
    user_result = cursor.fetchone()
    if not user_result:
        cursor.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with email: {request.username} is not found')
    cursor.close()
    verify_password = Hash.verify_password(request.password,user_result[3])
    if verify_password == False:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Incorrect password')
    #generate jwt token
    #pip install python-jose
    access_token = authToken.create_access_token(
        data={"sub": user_result[2]}
    )
    
    return {"access_token":access_token, "token_type":"bearer"}
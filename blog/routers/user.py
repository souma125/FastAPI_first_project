from fastapi import APIRouter,status,HTTPException,Response
import schemas
from database import conn
from hashing import Hash

router = APIRouter(
    prefix='/user',
    tags=['User']
) 

@router.post('/')
def create_user(request:schemas.User):
   cursor = conn.cursor()
   hashed_password = Hash.hash_password(request.password)
   query = "INSERT INTO user (name,email,password) VALUES (%s, %s,%s)"
   cursor.execute(query, (request.name, request.email,hashed_password))
   conn.commit()
   cursor.close()
   return {"message": "User added successfully"}

@router.get('/{id}',status_code=status.HTTP_200_OK)
def get_user(id:int):# -> dict[str, ToPythonOutputTypes | Any]:
   cursor = conn.cursor(buffered=True)
   query = f"SELECT u.id,u.name,u.email,b.title,b.body FROM user as u RIGHT JOIN blog as b ON b.user_id = u.id WHERE u.id = {id}"
   cursor.execute(query)
   conn.commit()
   results = cursor.fetchall()
   
   if not results:
      # response.status_code = status.HTTP_404_NOT_FOUND
      # return {'detail':f'Blog with id : {id} is not available'}
      cursor.close()
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id : {id} is not available')
   cursor.close()
   user_data = {
      'user id': results[0][0],  
      'user name': results[0][1],  
      'user email': results[0][2], 
      'blogs': [{'title': result[3], 'body': result[4]} for result in results]
   }
   return user_data

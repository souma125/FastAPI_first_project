from fastapi import APIRouter,status,HTTPException,Response
import schemas
from database import conn

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)

@router.get('/')
def all(status=status.HTTP_200_OK):
    cursor = conn.cursor(buffered=True)
    query = "SELECT b.title,b.body,u.id,u.name,u.email FROM blog as b JOIN user as u ON u.id = b.user_id"
    cursor.execute(query)
    conn.commit()
    results = cursor.fetchall()
    cursor.close()
    return {"blog": results}

@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog):
   cursor = conn.cursor()
   query = "INSERT INTO blog (title, body, user_id) VALUES (%s, %s, %s)"
   cursor.execute(query, (request.title, request.body, request.user_id))
   conn.commit()
   return {"message": "Blog added successfully"}

@router.get('/{id}',status_code=status.HTTP_200_OK)
def show(id:int,response:Response):
   cursor = conn.cursor(buffered=True)
   query = f"SELECT b.title,b.body,u.id,u.name,u.email FROM blog as b LEFT JOIN user as u ON u.id = b.user_id WHERE b.id = {id}"
   cursor.execute(query)
   conn.commit()
   results = cursor.fetchone()
   if not results:
      # response.status_code = status.HTTP_404_NOT_FOUND
      # return {'detail':f'Blog with id : {id} is not available'}
      cursor.close()
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id : {id} is not available')
   cursor.close()
   blog_data = {
      'title':results[0],
      'body':results[1],
      'creator':{
         'user id':results[2],
         'user name':results[3],
         'user email': results[4]
      }
   }
   return blog_data

@router.delete('/{id}')
def destroy(id):
   cursor = conn.cursor(buffered=True)
   select_query = f"SELECT id FROM blog WHERE id = {id}"
   cursor.execute(select_query)
   del_id = cursor.fetchone()
   if not del_id:
      cursor.close()
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id :{id} not found')
   delete_query = f"DELETE FROM blog where id = {del_id[0]}"
   cursor.execute(delete_query)
   result = cursor.rowcount
   conn.commit()
   cursor.close()
   if result <= 0:
      cursor.close()
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='Something went wrong')
   cursor.close()
   return {"message": f"Blog with {id} deleted successfully"}

@router.put('/{id}')
def modify(id,request:schemas.Blog):
   cursor = conn.cursor(buffered=True)
   select_query = f"SELECT id FROM blog WHERE id = {id}"
   cursor.execute(select_query)
   update_details = cursor.fetchone()
   if not update_details:
      cursor.close()
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id :{id} not found')
   update_query = f"UPDATE blog SET title = '{request.title}',body = '{request.body}' WHERE id = {id}"
   cursor.execute(update_query)
   result = cursor.rowcount
   conn.commit()
   if result <= 0:
      cursor.close()
      raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,detail='Update failed')
   fetch_updated_sql = f"SELECT * FROM blog WHERE id = {id}"
   cursor.execute(fetch_updated_sql)
   fetch_updated_data = cursor.fetchone()
   cursor.close()
   return {"blog": fetch_updated_data}
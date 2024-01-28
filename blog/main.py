# tutorial link: https://techwasti.com/fastapi-mysql-simple-rest-api-example
from fastapi import FastAPI

from routers import blog,user,login
# import hashing

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)
# pip install bcrypt(not working for the interpreter)
# pip install passlib(not working for the interpreter)





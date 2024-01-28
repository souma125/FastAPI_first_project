from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str
    user_id:int

#response model
# class ShowBlog(Blog):
#     blog: Blog
#     class Config():
#         orm_mode=True
        
class User(BaseModel):
    name:str
    email:str
    password:str
    
# class ShowUser(BaseModel):
#     name:str
#     email:str
class Login(BaseModel):
    username:str
    password:str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

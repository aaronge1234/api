from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
import app.models as models
import app.schemas as schemas
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.utils import hash
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
    return {"message" : "Hello World!"}


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='12345', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection success')
#         break
#     except Exception as error:
#         print("Connection failed, Error:", error)
#         time.sleep(2)



# @app.put("/posts/{id}")
# def update_posts(id: int, post: Post):
#     cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *"""
#                     ,(post.title, post.content, post.published, id))
#     update_posts = cursor.fetchone()
#     conn.commit()
#     if update_posts == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND
#                             ,detail= f"post with id: {id} does not exist!")


#     return {"message": "update", "data":update_posts}


#--------------------------------------------------------------------------------------------------------------

# my_post = [{'title':'title1', 'content':'content','id':1}, {'title':'title2', 'content':'content2','id':2}]

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i

# @app.post("/createposts")
# def create_posts(msg: dict = Body(...)):
#     print(msg)
#     return {"message": "successfully created posts!", "new_post": msg}

#title : string, content: string



# my_post = [{'title':'title1', 'content':'content','id':1}, {'title':'title2', 'content':'content2','id':2}]

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i

# @app.get('/')
# async def root():
#     return {"message" : "Hello World!"}

# @app.get('/posts')
# def get_posts():
#     return {"data": my_post}
#     # return {"data":"This is your posts"}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post = Body(...)):
#     # print(post)

#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 10000000)
#     my_post.append(post_dict)
#     return {"new_post": post_dict}

# @app.get("/posts/latest") #will go to post/{id} first
# def get_post_late():
#     return {'latest post' : my_post[len(my_post)-1]}

# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):

#     post = find_post(id) #check varible type
#     if not post:

#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND 
#                             ,detail=f'post with id:{id} was not found')
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f'post with id:{id} was not found'}
#     return {'id':id, 'post':post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     ind = find_index_post(id)
#     if ind == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND
#                             ,detail= f"post with id: {id} does not exist!")
    
#     my_post.pop(ind)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#         #return {"message": "Post deleted!"}


# @app.put("/posts/{id}")
# def update_posts(id: int, post: Post):
#     ind = find_index_post(id)
#     if ind == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND
#                             ,detail= f"post with id: {id} does not exist!")
#     post_dict = dict(post)
#     post_dict["id"] = id
#     my_post[ind] = post_dict

#     return {"message": "update", "data":post_dict}




# # @app.post("/createposts")
# # def create_posts(msg: dict = Body(...)):
# #     print(msg)
# #     return {"message": "successfully created posts!", "new_post": msg}

# #title : string, content: string
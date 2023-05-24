from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
import json

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get('/')
        #, response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):


    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        # .filter(models.Post.owner_id == current_user.id).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    result = []
    for i in results:
        print(i)
        result.append(dict({"Post": i[0], "Vote":i[1]}))
    # results = {results[i] : results[i] for i, _ in enumerate(inputTuple_2)}
    
    print(result)
    result2 = [{"Posts": l[0], "Vote":l[1]} for l in results]
    return result2

    # return dict(zip(["Post", "Vote"], results)) 

    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # return {"data": posts}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # print(current_user.email)
    
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
# def create_posts(post: Post = Body(...)):
    # cursor.execute("""insert into posts (title, content, published) values (%s,%s,%s) RETURNING * """
    #                ,(post.title, post.content, post.published) )
    # new_post = cursor.fetchone()

    # conn.commit() # push changes to update

    # return {"new_post": new_post}

@router.get("/{id}")
def get_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND
                            ,detail= f"post with id: {id} does not exist!")


    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform!")

    print(post)
    return dict(zip(["Post", "Vote"], post)) 

# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("""select * from posts where id = %s""", (str(id)))
#     post = cursor.fetchone()
#     if post == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND
#                             ,detail= f"post with id: {id} does not exist!")

#     return {'id':id, 'post':post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()
    if post== None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND
                            ,detail= f"post with id: {id} does not exist!")
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
    
#     cursor.execute("""delete from posts where id = %s returning * """, (str(id)))
#     post = cursor.fetchone()
#     conn.commit()

#     if post == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND
#                             ,detail= f"post with id: {id} does not exist!")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
        #return {"message": "Post deleted!"}

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id==id)

    post1 = post_query.first()
    
    if post1 == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND
                            ,detail= f"post with id: {id} does not exist!")
    
    if post1.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform!")

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
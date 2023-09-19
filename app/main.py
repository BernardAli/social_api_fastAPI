from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from random import randrange
import time
from . import models, schema
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='social_api', user='allgift',
                                password='Matt6:33', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error ", error)
        time.sleep(5)

my_posts = [
    {
        "id": 1,
        "title": "Best car brands",
        "content": "Toyota ranks at the top",
        "rating": 4
    },
    {
        "id": 2,
        "title": "Best Offroader",
        "content": "Nissan Patrol",
        "rating": 5
    },
    {
        "id": 3,
        "title": "Best SUV",
        "content": "Lexus R350",
        "rating": 4
    }
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Social Media APIs"}


@app.get("/posts/", response_model=List[schema.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    post = db.query(models.Post).all()
    return post


@app.post("/posts/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post: schema.CreatePost, db: Session = Depends(get_db)):
    # new_post = dict(post)
    # new_post['id'] = randrange(1, 10e10)
    # my_posts.append(new_post)
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schema.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # post = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    # my_posts.pop(index)
    # conn.commit()
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schema.PostResponse)
def get_post(id: int, updated_post: schema.UpdatePost, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # cursor.execute(""" UPDATE posts
    #                 SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    # post_dict = dict(post)
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # conn.commit()
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

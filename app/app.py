from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate
from app.db import Post, get_async_session, create_db_and_tables
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/hello-world")
def hello_world():
    return {"Hello": "World"}

text_posts = {"1": {"title": "First Post", "content": "This is the first post"},
              "2": {"title": "Second Post", "content": "This is the second post"},
              "3": {"title": "Third Post", "content": "This is the third post"},
              "4": {"title": "Fourth Post", "content": "This is the fourth post"},
              "5": {"title": "Fifth Post", "content": "This is the fifth post"},
              "6": {"title": "Sixth Post", "content": "This is the sixth post"},
              "7": {"title": "Seventh Post", "content": "This is the seventh post"},
              "8": {"title": "Eighth Post", "content": "This is the eighth post"},
              "9": {"title": "Ninth Post", "content": "This is the ninth post"},
              "10": {"title": "Tenth Post", "content": "This is the tenth post"}
            }

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if str(id) not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts[str(id)]


@app.post("/posts")
def create_post(post: PostCreate):
    new_id = str(len(text_posts) + 1)
    text_posts[new_id] = {"title": post.title, "content": post.content}
    return text_posts[new_id]
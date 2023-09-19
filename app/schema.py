from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True

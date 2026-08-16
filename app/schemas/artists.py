from pydantic import BaseModel, Field

class ArtistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)

class ArtistResponse(BaseModel):
    id: int
    name: str

class ArtistUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
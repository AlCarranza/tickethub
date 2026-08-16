from fastapi import APIRouter, HTTPException, status
from app.schemas.artists import ArtistCreate, ArtistResponse, ArtistUpdate

next_artist_id = 1
artists_db = []

router = APIRouter(
    prefix="/api/v1/artists",
    tags=["Artists"]
)

@router.get(
    "/", 
    status_code=status.HTTP_200_OK,
    response_model= list[ArtistResponse]
)
def get_artists():
    return artists_db

@router.get(
    "/{artist_id}", 
    status_code=status.HTTP_200_OK,
    response_model=ArtistResponse
)
def get_artist(artist_id: int):
    curr_artist = None

    for artist in artists_db:
        if artist["id"] == artist_id:
            curr_artist = artist
            break

    if curr_artist:
        return curr_artist
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artist {artist_id} not found"
        )

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED
)
def create_artist(artist: ArtistCreate):
    global next_artist_id
    artist_name = artist.name.strip()

    for existing_artist in artists_db:
        if existing_artist["name"].strip().lower() == artist_name.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Artist already exists"
            )

    new_artist = {
        "id": next_artist_id,
        "name": artist_name
    }

    artists_db.append(new_artist)

    next_artist_id += 1

    return new_artist

@router.put(
    "/{artist_id}",
    status_code=status.HTTP_200_OK,
    response_model=ArtistResponse
)
def update_artist(artist_id: int, artist: ArtistUpdate):
    target_artist = None
    new_name = artist.name.strip()

    for existing_artist in artists_db:
        if existing_artist["id"] == artist_id:
            target_artist = existing_artist
            break

    if not target_artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artist {artist_id} not found"
        )

    for existing_artist in artists_db:
        if existing_artist["id"] != artist_id:
            if existing_artist["name"].strip().lower() == new_name.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Artist already exists"
                )

    target_artist["name"] = new_name

    return target_artist
        
            


@router.delete(
    "/{artist_id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_artist(artist_id: int):
    for index, artist in enumerate(artists_db):
        if artist["id"] == artist_id:
            artists_db.pop(index)
            return
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Artist {artist_id} not found"
    )

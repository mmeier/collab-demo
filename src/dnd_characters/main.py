from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from dnd_characters.models import Character
from dnd_characters.storage import CharacterStorage


app = FastAPI(title="D&D Character API")
storage = CharacterStorage()


class CharacterCreate(BaseModel):
    character_name: str
    player_name: str


class CharacterUpdate(BaseModel):
    character_name: str
    player_name: str


@app.post("/characters", response_model=Character, status_code=status.HTTP_201_CREATED)
def create_character(character_data: CharacterCreate):
    character = Character(
        character_name=character_data.character_name,
        player_name=character_data.player_name
    )
    return storage.create(character)


@app.get("/characters", response_model=list[Character])
def list_characters():
    return storage.list_all()


@app.get("/characters/{character_id}", response_model=Character)
def get_character(character_id: str):
    character = storage.get(character_id)
    if character is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )
    return character


@app.put("/characters/{character_id}", response_model=Character)
def update_character(character_id: str, character_data: CharacterUpdate):
    character = Character(
        id=character_id,
        character_name=character_data.character_name,
        player_name=character_data.player_name
    )
    updated = storage.update(character_id, character)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )
    return updated


@app.delete("/characters/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: str):
    deleted = storage.delete(character_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )

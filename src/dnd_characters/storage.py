from typing import Optional
from dnd_characters.models import Character


class CharacterStorage:
    def __init__(self):
        self._characters: dict[str, Character] = {}

    def create(self, character: Character) -> Character:
        if character.id in self._characters:
            raise ValueError(f"Character with id {character.id} already exists")
        self._characters[character.id] = character
        return character

    def get(self, character_id: str) -> Optional[Character]:
        return self._characters.get(character_id)

    def list_all(self) -> list[Character]:
        return list(self._characters.values())

    def update(self, character_id: str, character: Character) -> Optional[Character]:
        if character_id not in self._characters:
            return None
        self._characters[character_id] = character
        return character

    def delete(self, character_id: str) -> bool:
        if character_id not in self._characters:
            return False
        del self._characters[character_id]
        return True

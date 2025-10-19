import pytest
from uuid import UUID
from pydantic import ValidationError
from dnd_characters.models import Character


class TestCharacterModel:
    def test_create_character_with_all_fields(self):
        character = Character(
            id="550e8400-e29b-41d4-a716-446655440000",
            character_name="Gandalf",
            player_name="Alice"
        )

        assert character.id == "550e8400-e29b-41d4-a716-446655440000"
        assert character.character_name == "Gandalf"
        assert character.player_name == "Alice"

    def test_create_character_without_id_generates_id(self):
        character = Character(
            character_name="Frodo",
            player_name="Bob"
        )

        assert character.id is not None
        assert len(character.id) > 0
        assert character.character_name == "Frodo"
        assert character.player_name == "Bob"

    def test_character_name_required(self):
        with pytest.raises(ValidationError) as exc_info:
            Character(player_name="Charlie")

        assert "character_name" in str(exc_info.value)

    def test_player_name_required(self):
        with pytest.raises(ValidationError) as exc_info:
            Character(character_name="Legolas")

        assert "player_name" in str(exc_info.value)

    def test_character_to_dict(self):
        character = Character(
            id="550e8400-e29b-41d4-a716-446655440000",
            character_name="Aragorn",
            player_name="Dave"
        )

        char_dict = character.model_dump()

        assert char_dict["id"] == "550e8400-e29b-41d4-a716-446655440000"
        assert char_dict["character_name"] == "Aragorn"
        assert char_dict["player_name"] == "Dave"

    def test_two_characters_with_different_ids_are_not_equal(self):
        char1 = Character(
            id="550e8400-e29b-41d4-a716-446655440000",
            character_name="Gimli",
            player_name="Eve"
        )
        char2 = Character(
            id="550e8400-e29b-41d4-a716-446655440001",
            character_name="Gimli",
            player_name="Eve"
        )

        assert char1.id != char2.id

import pytest
from dnd_characters.models import Character
from dnd_characters.storage import CharacterStorage


@pytest.fixture
def storage():
    return CharacterStorage()


@pytest.fixture
def sample_character():
    return Character(
        id="test-id-1",
        character_name="Tiamat",
        player_name="Frank"
    )


class TestCharacterStorage:
    def test_create_character(self, storage, sample_character):
        result = storage.create(sample_character)

        assert result.id == sample_character.id
        assert result.character_name == sample_character.character_name
        assert result.player_name == sample_character.player_name

    def test_get_character_by_id(self, storage, sample_character):
        storage.create(sample_character)
        result = storage.get(sample_character.id)

        assert result is not None
        assert result.id == sample_character.id
        assert result.character_name == sample_character.character_name

    def test_get_nonexistent_character_returns_none(self, storage):
        result = storage.get("nonexistent-id")
        assert result is None

    def test_list_all_characters_empty(self, storage):
        characters = storage.list_all()
        assert characters == []

    def test_list_all_characters(self, storage):
        char1 = Character(id="id-1", character_name="Char1", player_name="Player1")
        char2 = Character(id="id-2", character_name="Char2", player_name="Player2")

        storage.create(char1)
        storage.create(char2)

        characters = storage.list_all()
        assert len(characters) == 2
        assert any(c.id == "id-1" for c in characters)
        assert any(c.id == "id-2" for c in characters)

    def test_update_character(self, storage, sample_character):
        storage.create(sample_character)

        updated_character = Character(
            id=sample_character.id,
            character_name="Updated Name",
            player_name="Updated Player"
        )

        result = storage.update(sample_character.id, updated_character)

        assert result is not None
        assert result.id == sample_character.id
        assert result.character_name == "Updated Name"
        assert result.player_name == "Updated Player"

    def test_update_nonexistent_character_returns_none(self, storage):
        character = Character(
            id="nonexistent",
            character_name="Test",
            player_name="Test"
        )
        result = storage.update("nonexistent", character)
        assert result is None

    def test_delete_character(self, storage, sample_character):
        storage.create(sample_character)
        result = storage.delete(sample_character.id)

        assert result is True
        assert storage.get(sample_character.id) is None

    def test_delete_nonexistent_character_returns_false(self, storage):
        result = storage.delete("nonexistent-id")
        assert result is False

    def test_create_duplicate_id_raises_error(self, storage, sample_character):
        storage.create(sample_character)

        duplicate = Character(
            id=sample_character.id,
            character_name="Different Name",
            player_name="Different Player"
        )

        with pytest.raises(ValueError) as exc_info:
            storage.create(duplicate)

        assert "already exists" in str(exc_info.value).lower()

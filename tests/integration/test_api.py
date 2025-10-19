import pytest
from fastapi.testclient import TestClient
from dnd_characters.main import app, storage


@pytest.fixture(autouse=True)
def clear_storage():
    storage._characters.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)


class TestCharacterAPI:
    def test_create_character(self, client):
        response = client.post(
            "/characters",
            json={
                "character_name": "Elminster",
                "player_name": "Alice"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["character_name"] == "Elminster"
        assert data["player_name"] == "Alice"

    def test_create_character_missing_character_name(self, client):
        response = client.post(
            "/characters",
            json={"player_name": "Bob"}
        )

        assert response.status_code == 422

    def test_create_character_missing_player_name(self, client):
        response = client.post(
            "/characters",
            json={"character_name": "Raistlin"}
        )

        assert response.status_code == 422

    def test_get_character_by_id(self, client):
        create_response = client.post(
            "/characters",
            json={
                "character_name": "Drizzt",
                "player_name": "Charlie"
            }
        )
        created_id = create_response.json()["id"]

        get_response = client.get(f"/characters/{created_id}")

        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == created_id
        assert data["character_name"] == "Drizzt"
        assert data["player_name"] == "Charlie"

    def test_get_nonexistent_character(self, client):
        response = client.get("/characters/nonexistent-id")
        assert response.status_code == 404

    def test_list_all_characters_empty(self, client):
        response = client.get("/characters")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_all_characters(self, client):
        client.post(
            "/characters",
            json={"character_name": "Char1", "player_name": "Player1"}
        )
        client.post(
            "/characters",
            json={"character_name": "Char2", "player_name": "Player2"}
        )

        response = client.get("/characters")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        char_names = [c["character_name"] for c in data]
        assert "Char1" in char_names
        assert "Char2" in char_names

    def test_update_character(self, client):
        create_response = client.post(
            "/characters",
            json={"character_name": "Mordenkainen", "player_name": "Dave"}
        )
        character_id = create_response.json()["id"]

        update_response = client.put(
            f"/characters/{character_id}",
            json={
                "character_name": "Updated Mordenkainen",
                "player_name": "Updated Dave"
            }
        )

        assert update_response.status_code == 200
        data = update_response.json()
        assert data["id"] == character_id
        assert data["character_name"] == "Updated Mordenkainen"
        assert data["player_name"] == "Updated Dave"

    def test_update_nonexistent_character(self, client):
        response = client.put(
            "/characters/nonexistent-id",
            json={"character_name": "Test", "player_name": "Test"}
        )
        assert response.status_code == 404

    def test_delete_character(self, client):
        create_response = client.post(
            "/characters",
            json={"character_name": "Venger", "player_name": "Eve"}
        )
        character_id = create_response.json()["id"]

        delete_response = client.delete(f"/characters/{character_id}")
        assert delete_response.status_code == 204

        get_response = client.get(f"/characters/{character_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_character(self, client):
        response = client.delete("/characters/nonexistent-id")
        assert response.status_code == 404

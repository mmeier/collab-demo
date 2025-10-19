from pydantic import BaseModel, Field
from uuid import uuid4


# The character model is defined as a pydantic model.
#
class Character(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    character_name: str
    player_name: str

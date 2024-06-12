from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime, UTC

@dataclass
class BaseRecord(object):
    _id: int = field(kw_only=True, default=None)
    _created_date_utc: datetime = field(kw_only=True, default=None)

    def __post_init__(self):
        if self._id is None:
            self._id = str(uuid4())
        if self._created_date_utc is None:
            self._created_date_utc = datetime.now(UTC)

@dataclass
class Preference(BaseRecord):
    user_id: int
    character_pref: dict
    def __post_init__(self):
        self._id = self.user_id
        super().__post_init__()
@dataclass
class Move(BaseRecord):
    game: str
    character: str
    move_id: int
    base_move_id: int
    properties: dict
    url: str = field(default=None)
    image: str = field(default=None)


@dataclass
class Character(BaseRecord):
    game: str
    character_name: str
    moves: list[Move]


@dataclass
class Combo(BaseRecord):
    user_id: str
    game: str
    character: str
    combo_string: str

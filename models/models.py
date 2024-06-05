class Preference:
    def __init__(self, id:str, character_pref:dict) -> None:
        self.id = id
        self.character_pref = character_pref

class Character:
    def __init__(self, character_name) -> None:
        self.character_name = character_name
        self.moves = []

class Move:
    def __init__(self, move_id, character, properties:dict, base_move_id, url = None, image = None) -> None:
        self.move_id = move_id
        self.character = character
        self.base_move_id = base_move_id
        self.properties = properties
        self.url = url
        self.image = image
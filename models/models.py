class Preference:
    def __init__(self, id:str, character_pref:dict) -> None:
        self.id = id
        self.character_pref = character_pref

class Character:
    def __init__(self, character_name) -> None:
        self.character_name = character_name
        self.moves = []

class Move:
    def __init__(self, move_id, character, game, properties:dict, base_move_id, url = None, image = None) -> None:
        self.move_id = move_id
        self.character = character
        self.base_move_id = base_move_id
        self.properties = properties
        self.url = url
        self.image = image
        self.game = game

class Combo:
    def __init__(self, user_id, game, character, combo_string) -> None:
        self.user_id = user_id
        self.game = game
        self.character = character
        self.combo_string = combo_string
class Wiki:
    @staticmethod
    def get_info_box(game, character):
        raise NotImplementedError()
    @staticmethod
    def get_move_data(game, character, move):
        raise NotImplementedError()
    

class MoveNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
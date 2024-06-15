from dataclasses import asdict
import pymongo
from models.models import Preference, Move, Combo

from wikis.exceptions import NotFound

DB_NAME = 'framedata'

class Database:

    def __init__(self, url) -> None:
        self.client = pymongo.MongoClient(url)
        self.db = self.client[DB_NAME]

    #section Preferences

    def add_preference(self, user_id, preference):
        self.db['preferences'].insert_one(asdict(Preference(user_id=user_id, character_pref=preference)))

    def get_preference(self, user_id) -> Preference:
        result = self.db['preferences'].find_one({'user_id': user_id})
        if result is not None:
            return Preference(**result)
        
    #endsection Preferences

    #section Character

    def add_character_data(self, data:list[Move]):
        self.db['moves'].insert_many([asdict(x) for x in data])
        
    def get_character_data(self, game, character, move) -> list[Move] | None:
        result = self.db['moves'].find_one({'game': game, 'character': character, 'move_id': move})
        if result is not None:
            return [Move(**result)]
        results = list(self.db['moves'].find({'game': game, 'character': character, 'base_move_id': move}))
        if len(results) == 0:
            return None
        else:
            return [Move(**x) for x in results]
        
    #endsection Character


    #section Combo

    def add_combo(self, user_id, game, character, combo_string):
        self.db['combos'].insert_one(asdict(Combo(user_id, game, character, combo_string)))

    def add_tag_to_combo(self, combo_id, tag):
        # combo_record = self.db['combos'].find_one({'_id': combo._id})
        # if combo_record is None:
        #     raise Exception
        # combo_record.tags.append(tag)
        self.db['combos'].update_one({'_id': combo_id}, {'$addToSet': {'tag': tag}})

    def remove_tag_from_combo(self, combo_id, tag):
        self.db['combos'].update_one({'_id': combo_id}, {'$pull': {'tag': tag}})

    
    def get_all_user_combos(self, user_id, game, character) -> list[Combo] | None:
        results = list(self.db['combos'].find({'user_id': user_id, 'game': game, 'character': character}).sort('_created_date_utc'))
        if len(results) == 0:
            return []
        else:
            return [Combo(**x) for x in results]
        
    def get_user_combos_with_tag(self, user_id, game, character, tag) -> list[Combo] | None:
        results = list(self.db['combos'].find({'user_id': user_id, 'game': game, 'character': character, 'tag': tag}).sort('_created_date_utc'))
        if len(results) == 0:
            return []
        else:
            return [Combo(**x) for x in results]

    def remove_combo(self, user_id, game, character, number:int):
        user_combos = self.get_all_user_combos(user_id, game, character)
        id_to_delete = user_combos[number]._id
        self.db['combos'].delete_one({'_id': id_to_delete})

    #endsection Combo
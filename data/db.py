import io
import json
import os
from models.move import Move

db_file_name = 'db.json' # totally a real database

if not os.path.exists(db_file_name):
    with open(db_file_name, 'w', encoding='utf-8') as f:
        json.dump({'prefs':[], 'characters':[]}, f)

class Preferences:

    def __init__(self) -> None:
        pass

    def add_preference(self, id, preference):
        with open(db_file_name, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        
        user_pref = [x for x in file_data['prefs'] if x['id'] == id]
        if len(user_pref) > 0:
            user_pref[0]['pref'] = preference
        else:
            file_data['prefs'].append({'id': id, 'pref': preference})

        with open(db_file_name, 'w', encoding='utf-8') as f:
            json.dump(file_data, f)

    def get_preference(self, id):
        with open(db_file_name, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
            user_pref = [x for x in file_data['prefs'] if x['id'] == id]
            if len(user_pref) > 0:
                return user_pref[0]['pref']
            return None
        
class CharacterData:

    def add_character_data(self, character:str, move:str, data:list):
        with open(db_file_name, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        character_obj = [x for x in file_data['characters'] if x['name'] == character]
        if len(character_obj) > 0:
            character_obj = character_obj[0]
        else:
            character_obj = {'name': character, 'moves': []}
            file_data['characters'].append(character_obj)
        
        move_record = [x for x in character_obj['moves'] if x['name'] == move]
        if len(move_record) > 0:
            move_record = move_record[0]
        else:
            move_record = {'name': move}
            character_obj['moves'].append(move_record)
        move_record['data'] = [x.toJSON() for x in data]

        with open(db_file_name, 'w', encoding='utf-8') as f:
            json.dump(file_data, f)
        
    def get_character_data(self, character, move):
        with open(db_file_name, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        try:
            return [Move(data=z) for z in [y for y in [x for x in file_data['characters'] if x['name'] == character][0]['moves'] if y['name'] == move][0]['data']]
        except Exception:
            return None
        
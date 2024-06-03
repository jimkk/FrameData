import io
import json
import os

db_file_name = 'db.json' # totally a real database

class Preferences:

    def __init__(self) -> None:
        if not os.path.exists(db_file_name):
            with open(db_file_name, 'w', encoding='utf-8') as f:
                json.dump({'prefs':[]}, f)

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
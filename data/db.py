import io
import json
import os
from ravendb import DocumentStore
from models.models import *

database_name = 'framedata'

class Database:

    document_store: DocumentStore = None

    def __init__(self, url) -> None:
        self.document_store = DocumentStore(url, database_name)
        self.document_store.initialize()

    def add_preference(self, id, preference):
        with self.document_store.open_session() as session:
            session.store(Preference(id, preference), "Preferences/" + str(id))
            session.save_changes()

    def get_preference(self, id) -> Preference:
        with self.document_store.open_session() as session:
            pref = session.load("Preferences/" + str(id))
            if pref is not None:
                return pref
        
    def add_character_data(self, game:str, character:str, move:str, data:list[Move], url=None, image=None):
        with self.document_store.open_session() as session:
            for m in data:
                m.base_move_id = move
                session.store(m)
            session.save_changes()
        
    def get_character_data(self, game, character, move) -> Move:
        with self.document_store.open_session() as session:
            # Try for specific move
            move_list = list(session.query_collection('Moves').where_equals('move_id', move))
            if len(move_list) > 0:
                return move_list
            move_list = session.query_collection('Moves').where_equals('base_move_id', move)
            # move_record = session.load("move/" + game + "_" + character + "_" + move)
            # if move_record is None:
            #     return None
            return list(move_list)
        
import io
import json
import os
from ravendb import DocumentStore, GetDatabaseNamesOperation, CreateDatabaseOperation
from ravendb.serverwide.database_record import DatabaseRecord
from ravendb.documents.queries.query import QueryOperator
from models.models import *

database_name = 'framedata'

class Database:

    document_store: DocumentStore = None

    def __init__(self, url) -> None:
        self.document_store = DocumentStore(url, database_name)
        self.document_store.initialize()
        databaseNames = self.document_store.maintenance.server.send(GetDatabaseNamesOperation(0,20))
        if 'framedata' not in databaseNames:
            self.document_store.maintenance.server.send(CreateDatabaseOperation(DatabaseRecord('framedata')))

    #section Preferences
    def add_preference(self, user_id, preference):
        with self.document_store.open_session() as session:
            session.store(Preference(user_id, preference), "Preferences/" + str(user_id))
            session.save_changes()

    def get_preference(self, user_id) -> Preference:
        with self.document_store.open_session() as session:
            pref = session.load("Preferences/" + str(user_id))
            if pref is not None:
                return pref
    
    #endsection Preferences

    #section Character

    def add_character_data(self, move:str, data:list[Move]):
        with self.document_store.open_session() as session:
            for m in data:
                m.base_move_id = move
                session.store(m)
            session.save_changes()
        
    def get_character_data(self, game, character, move) -> Move:
        with self.document_store.open_session() as session:
            # Try for specific move
            move_list = list(session.query_collection('Moves').where_equals('move_id', move).and_also().where_equals('character', character).and_also().where_equals('game', game))
            if len(move_list) > 0:
                return move_list
            move_list = session.query_collection('Moves').where_equals('base_move_id', move).and_also().where_equals('character', character).and_also().where_equals('game', game)
            # move_record = session.load("move/" + game + "_" + character + "_" + move)
            # if move_record is None:
            #     return None
            return list(move_list)
    
    #endsection Character

    #section Combo

    def add_combo(self, user_id, combo_string):
        with self.document_store.open_session() as session:
            session.store(Combo(user_id, combo_string))
            session.save_changes()
    
    def get_all_user_combos(self, user_id):
        with self.document_store.open_session() as session:
            combo_list = list(session.query_collection('Comboes').where_equals('user_id', user_id))
            return combo_list

    def remove_combo(self, number:int):
        with self.document_store.open_session() as session:
            combo = session.query_collection('Comboes').skip(number).first()
            session.delete(combo)
            session.save_changes()

    #endsection Combo
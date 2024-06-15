import requests
import re
from bs4 import BeautifulSoup
from models.models import Move
from wikis.base import Wiki
from wikis.exceptions import NotFound

url = 'https://wiki.supercombo.gg'

games = {
    'sf6': 'Street_Fighter_6'
}
class SuperCombo(Wiki):
    @staticmethod
    def get_info_box(game, character):
        r = requests.get(url + '/w/' + games[game] + '/' + character)

        data = BeautifulSoup(r.content, 'html.parser')

        infobox = data.find("table", class_='infobox')

        properties = {}
        for property in infobox.find_all('tr'):
            if property.th and property.td:
                properties[property.th.text.strip()] =  property.td.text.strip()

        return properties
    @staticmethod
    def get_move_data(game, character, move_id):
        r = requests.get(url + '/w/' + games[game] + '/' + character)

        data = BeautifulSoup(r.content, 'html.parser')

        move_list = [x['id'] for x in data.find_all('span', class_='mw-headline') if re.search(r'[0-9]', x['id']) is not None]

        # move_dict = {re.search(r'[j]*[0-9.]+[A-Z]+', x).group(): x for x in move_list}

        move_dict = {}
        for x in move_list:
            key = x
            if '(' in x:
                key = re.search(r'\((.*)\)', x).groups()[0]
            move_dict[key] = x
            
            # re.search(r'[j]*[0-9.]+[A-Z]+', x).group()
        try:
            move_data = data.find(attrs={'id':move_dict[move_id]})
        except KeyError as ex:
            raise NotFound() from ex
        
        # if move_data is None:
        #     raise Exception('Move not found')

        move_data = move_data.parent.next_sibling.next_sibling

        move_data_tables = move_data.find_all('table')
        move_subtypes = move_data.find_all('div', class_='movedata-flex-framedata-name-item')
        moves = []
        for i, move_data_table in enumerate(move_data_tables):
            data_columns = move_data_table.find_all('th')
            data_values = move_data_table.find_all('td') 
            move_properties = {}
            for j, col in enumerate(data_columns):
                move_properties[col.text.strip()] =  data_values[j].text.strip()
            move = Move(game, character, move_subtypes[i*2].div.text, move_id,  move_properties)

            # move.name = move_dict[move_id].replace('_', ' ')
            move.image = url + move_data.a.img.attrs['src']
            move.url = url + '/w/' + games[game] + '/' + character + '#' + move_id

            moves.append(move)

        return moves
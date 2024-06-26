# import requests
# import re
# from bs4 import BeautifulSoup
# from wikis.base import Wiki

# url = 'https://dustloop.com'

# games = {
#     'ggst': 'GGST'
# }
# class DustLoop(Wiki):
#     @staticmethod
#     def get_info_box(game, character):
#         r = requests.get(url + '/w/' + games[game] + '/' + character)

#         data = BeautifulSoup(r.content, 'html.parser')

#         infobox = data.find("table", class_='infobox')

#         properties = {}
#         for property in infobox.find_all('tr'):
#             if property.th and property.td:
#                 properties[property.th.text.strip()] =  property.td.text.strip()

#         return properties
#     @staticmethod
#     def get_move_data(game, character, move_id):
#         r = requests.get(url + '/w/' + games[game] + '/' + character)

#         data = BeautifulSoup(r.content, 'html.parser')

#         move_list = [x for x in data.find_all('span', class_='mw-headline') if x is not None]

#         # move_dict = {re.search(r'[j]*[0-9.]+[A-Z]+', x).group(): x for x in move_list}

#         move_dict = {}
#         for x in move_list:
#             if re.match(r'([0-9]+|[a-z.])A-Z', x['id']):
#                 # Normal Move
#                 pass
#             if x.find_parent('h3').find_next_sibling('div').name == 'p':
#                 key = x.parent.next_sibling.span.b.span.text
#                 move_dict[key] = x['id']
            
#             # re.search(r'[j]*[0-9.]+[A-Z]+', x).group()

#         move_data = data.find(attrs={'id':move_dict[move_id]})
        
#         if move_data is None:
#             raise Exception('Move not found')

#         move_data = move_data.parent.next_sibling

#         move_data_tables = move_data.find_all('table')
#         move_subtypes = move_data.find_all('div', class_='movedata-flex-framedata-name-item')
#         moves = []
#         for i, move_data_table in enumerate(move_data_tables):
#             move = Move(move_subtypes[i*2].div.text)
#             data_columns = move_data_table.find_all('th')
#             data_values = move_data_table.find_all('td') 
#             for i, col in enumerate(data_columns):
#                 move.add_property(col.text.strip(), data_values[i].text.strip())

#             # move.name = move_dict[move_id].replace('_', ' ')
#             move.add_image_link(url + move_data.a.img.attrs['src'])
#             move.add_source(url + '/w/' + games[game] + '/' + character + '#' + move_id)

#             moves.append(move)

#         return moves
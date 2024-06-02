import requests
from bs4 import BeautifulSoup

url = 'https://wiki.supercombo.gg'

games = {
    'sf6': 'Street_Fighter_6'
}

def get_info_box(game, character):
    r = requests.get(url + '/w/' + games[game] + '/' + character)

    data = BeautifulSoup(r.content, 'html.parser')

    infobox = data.find("table", class_='infobox')

    properties = {}
    for property in infobox.find_all('tr'):
        if property.th and property.td:
            properties[property.th.text.strip()] =  property.td.text.strip()

    return properties

def get_move_data(game, character, move):
    r = requests.get(url + '/w/' + games[game] + '/' + character)

    data = BeautifulSoup(r.content, 'html.parser')

    move_data = data.find(attrs={'id':move}).parent.next_sibling.next_sibling

    move_data_table = move_data.find('table')

    properties = {}
    data_columns = move_data_table.find_all('th')
    data_values = move_data_table.find_all('td') 
    for i in range(len(data_columns)):
        properties[data_columns[i].text.strip()] = data_values[i].text.strip()

    properties['image'] = url + move_data.a.img.attrs['src']
    properties['url'] = url + '/w/' + games[game] + '/' + character + '#' + move

    return properties
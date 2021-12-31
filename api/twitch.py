import requests
from utils import Client_ID, access_token

URL_STREAM = 'https://api.twitch.tv/helix/streams?game_id='
URL_GAME = 'https://api.twitch.tv/helix/games?name='
URL_USER = 'https://api.twitch.tv/helix/users?id='

head = {
    'Client-ID': Client_ID,
    'Authorization': access_token()
}

def get_stream(name):
    response = []
    r = requests.get(URL_GAME+name, headers=head).json()['data']
    if(r):
        r = requests.get(URL_STREAM+r[0]['id'], headers=head).json()['data']
        if(r):
            response = formata_retorno(r)
            return response
        else:
            return 400
    else:
        return 400


def get_user_name(id):
    r = requests.get(URL_USER+id, headers=head).json()['data'][0]['login']
    if(r):
        return r
    else:
        return 400

def formata_retorno(json):
    response = []
    for stream in json:
        response.append({
            'titulo': stream['title'],
            'inicio': stream['started_at'],
            'user': 'https://www.twitch.tv/'+get_user_name(stream['user_id']),
            'idioma': stream['language'],
            'imagem': stream['thumbnail_url'].replace('{width}x{height}', '250x150'),
            'conteudo_adulto': stream['is_mature']
        })
    return response
import json
from igdb.wrapper import IGDBWrapper
from googleapiclient.discovery import build
from utils import Client_ID, access_token, API_KEY_YOUTUBE
from twitch import get_stream

DATA_GAME_INFO = 'where id = {0}; fields name, cover, genres, platforms, summary, url, aggregated_rating, first_release_date;'
DATA_COVERS = 'where id = {0}; fields url;'
DATA_PLATFORM_GENRES = 'where id = {0}; fields name;'
DATA_SEARCH = 'search "{0}"; fields cover, name, id; where version_parent = null; limit 50;'
YOUTUBE_URL = 'https://www.youtube.com/embed/'

wrapper = IGDBWrapper(Client_ID, access_token().replace('Bearer ', ''))


def get_games(name):
    response = []
    byte_array = wrapper.api_request('games', DATA_SEARCH.format(name))
    message = json.loads(byte_array)
    for game in message:
        response.append({
            'name': game['name'] if "name" in game else "",
            'cover': get_covers(game['cover'])if "cover" in game else 'https://images.igdb.com/igdb/image/upload/t_cover_big/nocover.png',
            'id': game['id']
        })
    return response


def get_game_info(id):
    response = []
    byte_array = wrapper.api_request('games', DATA_GAME_INFO.format(id))
    message = json.loads(byte_array)
    for game in message:
        genres = []
        platforms = []
        if "genres" in game:
            for i in game['genres']:
                genres.append(get_genre_platforms(i, 0))
        if "platforms" in game:
            for i in game['platforms']:
                platforms.append(get_genre_platforms(i, 1))

        response.append({
            'name': game['name'] if "name" in game else "",
            'url': game['url'] if "url" in game else "",
            'cover': get_covers(game['cover']) if "cover" in game else "",
            'generos': genres,
            'plataformas': platforms,
            'descricao': game['summary'] if "summary" in game else "",
            'avaliacao': game['aggregated_rating'] if "aggregated_rating" in game else 0,
            'youtube_id': get_trailer(game['name']),
            'data_criacao': game['first_release_date'] if "first_release_date" in game else "",
            'streams': get_stream(game['name'])
        })

    return response


def get_genre_platforms(id, tipo):
    byte_array = wrapper.api_request(
        'genres' if tipo == 0 else 'platforms', DATA_PLATFORM_GENRES.format(id))
    return json.loads(byte_array)[0]['name']


def get_covers(id):
    byte_array = wrapper.api_request('covers', DATA_COVERS.format(id))
    return json.loads(byte_array)[0]['url'].replace('t_thumb', 't_cover_big')


def get_trailer(nomeFilme):
    youtube = build('youtube', 'v3', developerKey=API_KEY_YOUTUBE)
    req = youtube.search().list(q=nomeFilme + "game trailer",
                                part='snippet', type='video', maxResults=1)
    resp = req.execute()
    if(len(resp['items'])) > 0:
        return YOUTUBE_URL+resp['items'][0]['id']['videoId']
    else:
        return ''

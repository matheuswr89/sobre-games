import json
from igdb.wrapper import IGDBWrapper
from utils import Client_ID, access_token

DATA_SEARCH = 'search "{0}"; fields name, cover, genres, platforms, summary, url, aggregated_rating; where version_parent = null;'
DATA_COVERS = 'where id = {0}; fields url;'
DATA_PLATFORM_GENRES = 'where id = {0}; fields name;'

wrapper = IGDBWrapper(Client_ID, access_token().replace('Bearer ', ''))


def get_games(name):
    response = []
    byte_array = wrapper.api_request('games', DATA_SEARCH.format(name))
    message = json.loads(byte_array)
    for game in message:
        genres = []
        platforms = []
        avaliacao = 0 if "aggregated_rating" not in game else game['aggregated_rating']
        if "genres" in game:
            for i in game['genres']:
                genres.append(get_genre_platforms(i, 0))
        if "platforms" in game:
            for i in game['platforms']:
                platforms.append(get_genre_platforms(i, 1))

        response.append({
            'name': game['name'],
            'url': game['url'],
            'cover': get_covers(game['cover']),
            'generos': genres,
            'plataformas': platforms,
            'descricao': game['summary'],
            'avaliacao': avaliacao
        })

    return response


def get_genre_platforms(id, tipo):
    byte_array = wrapper.api_request(
        'genres' if tipo == 0 else 'platforms', DATA_PLATFORM_GENRES.format(id))
    return json.loads(byte_array)[0]['name']


def get_covers(id):
    byte_array = wrapper.api_request('covers', DATA_COVERS.format(id))
    return json.loads(byte_array)[0]['url'].replace('t_thumb', 't_cover_big')

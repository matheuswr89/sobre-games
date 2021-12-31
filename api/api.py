import os
from flask import Flask
from flask_restful import request
from flask_cors import CORS
from game import get_game_info, get_games

app = Flask(__name__)
CORS(app)

@app.route('/')
def msg():
    return {'response': 'API sobe jogos de diversas plataformas e lives na twitch'}, 200


@app.route('/gameinfo')
def get_game():
    id = request.args.get('id')
    if id == "":
        return {'error': "Forneça o nome de um jogo."}, 400
    output = get_game_info(id)
    if output:
        return {'response': output}, 200
    else:
        return {'response': 'Nenhum jogo com esse nome foi encontrado.'}, 404

@app.route('/games')
def get_all_games():
    nome = request.args.get('name')
    if nome == "":
        return {'error': "Forneça o nome de um jogo."}, 400
    output = get_games(nome)
    if output:
        return {'response': output}, 200
    else:
        return {'response': 'Nenhum jogo com esse nome foi encontrado.'}, 404

if __name__ == '__main__':
    porta = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=porta,debug=True)
import os
from flask import Flask
from flask_restful import request
from flask_cors import CORS
from twitch import get_stream
from game import get_games

app = Flask(__name__)
CORS(app)

@app.route('/')
def msg():
    return {'response': 'Adicione /game?name=[nome jogo] para obter as informações de um jogo ou /stream?name=[nome jogo] para obter as lives do jogo.'}, 200


@app.route('/game')
def get_game():
    nome = request.args.get('name')
    if nome == "":
        return {'error': "Forneça o nome de um jogo."}, 400
    output = get_games(nome)
    if output:
        return {'response': output}, 200
    else:
        return {'response': 'Nenhum jogo com esse nome foi encontrado.'}, 404

@app.route('/stream')
def get_streams():
    nome = request.args.get('name')
    if nome == "":
        return {'error': "Forneça o nome de um jogo."}, 400
    output = get_stream(nome)
    if(output != 400):
        return {'response': output}, 200
    else:
        return {'response': 'Nenhuma stream para esse jogo foi encontrada.'}, 404

if __name__ == '__main__':
    porta = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=porta,debug=True)
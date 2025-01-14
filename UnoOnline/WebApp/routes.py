from WebApp import app
from flask import render_template,jsonify, request,session,redirect
from flask_socketio import join_room,leave_room,send,SocketIO
from scripts import game_logic # játékakciók
from scripts.game_db import dbHandler as db # adatbázis kapcsolat

game= game_logic.Game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game(player_list):
    # A játék elindítása itt történik...
    game.start_game(player_list)
    # A válaszban JSON adatot küldünk vissza
    return jsonify({
        'status': 'Game started',
        'players': game.players,
        'current_player': game.players[0]
    })

@app.route('/play_card', methods=['POST'])
def play_card():
    data = request.get_json()
    player = data.get('player')
    card = data.get('card')
    color = data.get('color')  # Ha van színválasztás
    
    # Ellenőrizzük, hogy a kártya a játékos kezében van-e, majd játsszuk le
    if card in game.player_hands[player]:
        game.play_card(player, card, color)
        return jsonify({
            'status': 'Card played',
            'next_player': game.next_player(),
            'player_hand': game.player_hands[player],
            'discard_pile': game.discard_pile
        })
    else:
        return jsonify({'status': 'Invalid card'}), 400

@app.route('/draw_card', methods=['POST'])
def draw_card():
    data = request.get_json()  # JSON adatokat olvasunk be
    player = data.get('player')

    # A kártya húzás logikája
    card = game.draw_card(player)

    return jsonify({
        'status': 'Card drawn',
        'card': card,
        'next_player': game.next_player(),
        'player_hand': game.player_hands[player]
    })

@app.route('/call_uno', methods=['POST'])
def call_uno():
    data = request.get_json()  # JSON adatokat olvasunk be
    player = data.get('player')
    
    # A játékban szereplő játékos és az UNO hívás logikája
    if player not in game.players:
        return jsonify({'status': 'Player not found'}), 400
    
    if game.call_uno(player):
        return jsonify({
            'status': 'UNO called successfully',
            'uno_called': True,
            'next_player': game.next_player(),
            'player_hand': game.player_hands[player]
        })
    else:
        return jsonify({
            'status': 'Cannot call UNO',
            'uno_called': False,
            'next_player': game.next_player(),
            'player_hand': game.player_hands[player]
        })

@app.route('/current_game_state', methods=['GET'])
def current_game_state():
    return jsonify({
        'players': game.players,
        'current_player': game.players[game.current_player],
        'discard_pile': game.discard_pile,
        'player_hands': {
            player: len(cards) if player != game.players[game.current_player] else cards
            for player, cards in game.player_hands.items()
        },
        'winner': game.winner,
        'current_color': game.current_color
    })
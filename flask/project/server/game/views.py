from flask import Blueprint, request, jsonify
from project.server.model_pony import Game, Group, Player, Stadistic
from randomuser import RandomUser
from pony.orm import *
import random
import requests
import json

soccer_game_blueprint = Blueprint("soccer", __name__)


def get_players():
    players = Player.select(lambda Player: Player)  # select * from Player
    return jsonify(players=[player.serializer for player in players])


def get_games():
    games = Game.select(lambda Game: Game)
    return jsonify(players=[game.serializer for game in games])


def get_groups():
    return Group.select(lambda Group: Group)


def generate_groups():
    with db_session:
        response = requests.get(
            'https://livescore-api.com/api-client/teams/list.json?key=JTodK1q8qB912pXO&secret=m0iLwUhdsbjX8KGRE55p6vxw6Hy97vYt')
        if response.status_code == 200:
            response_dicts = json.loads(response.content)
            for response_dict in response_dicts['data']['teams']:
                Group(name=response_dict['name'], alter_name='')

    return get_groups()


def generate_stadistic():
    with db_session:
        for _ in range(10):
            Stadistic(
                goals=random.randint(5),
                win=random.randint(10),
                lose=random.randint(20)
            )
    return Stadistic.select(lambda Stadistic: Stadistic)


def create_players():
    user_list = RandomUser.generate_users(10)
    stadistics = list(generate_stadistic())
    groups = list(generate_groups())
    with db_session:
        for user in user_list:
            Player(name=user.get_full_name(),
                   salary=random.randint(10),
                   group=random.choices(groups),
                   stadistic=random.choices(stadistics))


def generate_games():
    with db_session:
        response = requests.get(
            'https://livescore-api.com/api-client/scores/events.json?key=JTodK1q8qB912pXO&secret=m0iLwUhdsbjX8KGRE55p6vxw6Hy97vYt&id=129180')

        if response.status_code == 200:
            response_dicts = json.loads(response.content)
            for mach_id in response_dicts['data']['event']:
                response_mach = requests.get(
                    f'https://live-score-api.com/api-client/matches/stats.json?match_id={mach_id["match_id"]}&key=JTodK1q8qB912pXO&secret=m0iLwUhdsbjX8KGRE55p6vxw6Hy97vYt')
                if response_mach.status_code == 200:
                    response_mach_dicts = json.loads(response_mach.content)
                    game_data = response_mach_dicts['data']
                    groups = list(get_groups())
                    Game(time=random.randint(90),
                         score=random.randint(10),
                         yellow_cards=game_data['yellow_cards'],
                         goal_kicks=game_data['goal_kicks'],
                         dangerous_attacks=game_data['dangerous_attacks'],
                         group_one=random.choices(groups),
                         group_two=random.choices(groups))


@soccer_game_blueprint.route("/soccer/", methods=["GET", "POSt"])
def soccer_view():
    if request.method == 'GET':
        return get_players()


@soccer_game_blueprint.route("/soccer/create_player/", methods=["GET", ])
def player_view():
    if request.method == 'GET':
        create_players()
        return get_players()

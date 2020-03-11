from pony.orm import *

db = Database()


class Game(db.Entity):
    time = Required(float)
    score = Required(int)
    yellow_cards = Required(str)
    goal_kicks = Required(str)
    dangerous_attacks = Required(str)
    group_one = Set('Group', reverse='group_one')  # -> FK
    group_two = Set('Group', reverse='group_two')

    @property
    def serializer(self):
        return {
            'time': self.time,
            'score': self.score,
            'yellow_cars': self.yellow_cards,
            'goal_kicks': self.goal_kicks,
            'dangerous_attacks': self.dangerous_attacks,
            'group_one': self.group_one,
            'group_two': self.group_two
        }

    def __str__(self):
        return f'{self.group_one} vs {self.group_two}'


class Group(db.Entity):
    name = Required(str)
    alter_name = Optional(str)
    player = Set('Player')
    group_one = Set('Game', reverse='group_one')
    group_two = Set('Game', reverse='group_two')

    def __str__(self):
        return f'{self.name}'


class Player(db.Entity):
    name = Required(str)
    salary = Optional(float)
    group = Set('Group')
    stadistic = Set('Stadistic')

    @property
    def serializer(self):
        return {
            'name': self.name,
            'salary': self.salary,
            'group': self.group,
        }

    def __str__(self):
        return f'{self.name}'


class Stadistic(db.Entity):
    player = Set('Player')
    goals = Required(int)
    wins = Required(int)
    lose = Required(int)

    def __str__(self):
        return f'{self.player}'

POSTGRES_URL = 'rajje.db.elephantsql.com'
POSTGRES_USER = 'ewsdjkfb'
POSTGRES_PW = 'XPRIxkj4v2B6MZDLbVW6yvpFIHfSmltT'
POSTGRES_DB = 'ewsdjkfb'

db.bind(
    'postgres',
    user=POSTGRES_USER,
    password=POSTGRES_PW,
    host=POSTGRES_URL,
    database=POSTGRES_DB,
    port='5432'
)
# db.drop_all_tables(with_all_data=True)
db.generate_mapping(create_tables=True)


from model.user import User
from controller.graph import Graph
from gen.sdf.equations import Equation
from gen.sdf.factory import Factory
from view.plot import ViewSystem
from model.database import Database
import numexpr as ne
import os


# braches are menus
# leafs are actions
# NAVIGATION_TREE = [
#     [
#         "create publication"
#         "my publications",
#         "browse publications",
#         "export publication"
#     ]
# ]


class Action:
    def __init__(
            self,
            name: str,
            db_action_key: str,
            view_action_key: str,
            user_inputs: list[str] = []
    ):
        self.name = name
        self.db_action_key = db_action_key
        self.view_action_key = db_action_key  # view template which can be reused
        self.user_inputs = user_inputs


class Node:
    def __init__(self, name: str, actions: list[Action] = []):
        self.name
        self.actions = actions


NAV = Graph(
    [
        Node(
            "Log-In",
            [
                Action('Log-In', 'login', ['name', 'password']),
                Action('New-Acc', 'register', ['name', 'password']),
            ]
        ),
        Node(
            "Main Menu"
        ),
        Node(
            "Browse Publications"
        ),
        Node(
            "New Publication",
            ["Enter post text"]
        ),
        Node(
            "View Publication",
            ["rate", "comment"]
        ),
    ],
    [
        [1, 2],
        [],
        [],
    ]
)


class Engine:
    def __init__(self):
        self.user = None
        self.fac = Factory((28, 28, 28))
        self.pl = ViewSystem()
        # a stack that represents the user position in the navigation tree
        # self.user_pos = []
        self.path = []
        self.pos = 0

    # def run(self):
    #     eq = Equation(input())
    #     mesh = self.fac.get_mesh(eq)
    #     self.pl.draw_mesh(mesh)

    # def run(self):
        # print("Welcome, please log-in")
        # name = input('name: ')
        # password = input('password: ')
        # self.user = User(name, password)

    def is_choise_valid(self, choise_id):
        range_begin = int(len(self.path) == 0)
        return range_begin <= choise_id and choise_id <= NAV.degree(self.pos)

    def move(self, choise: int):
        if choise == 0:
            self.pos = self.path.pop()
        else:
            self.path.append(self.pos)
            self.pos = NAV.adj[self.pos][choise-1]

    def draw(self):
        os.system('cls')
        print('='*4 + NAV.nodes[self.pos] + '='*4)
        if len(self.path):
            print("0: back")
        for i, n in enumerate(NAV.adjacent(self.pos)):
            print(f"{i+1}: {n}")
        print('-'*16)

    def choose(self):
        while True:
            try:
                choise = int(input())
            except ValueError:
                print("Input an id for the menu window to enter")
                continue
            if not self.is_choise_valid(choise):
                print("Invalid id choise, try again")
                continue
            self.move(choise)
            break

    def run(self):
        while True:
            self.draw()
            self.choose()





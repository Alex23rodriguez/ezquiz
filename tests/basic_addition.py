from random import randint

from ezquiz import APIGame, Q


def get_ints():
    return randint(1, 10), randint(1, 10)


def ask_addition(t):
    a, b = t
    return f"what is {a} + {b}?"


def correct_addition(t):
    return t[0] + t[1]


AddQ = Q[tuple[int, int]](
    get_seed=get_ints,
    ask=ask_addition,
    correct=correct_addition,
)


def ask_mult(t):
    a, b = t
    return f"what is {a} * {b}?"


def correct_mult(t):
    a, b = t
    return a * b


MultQ = Q[tuple[int, int]](
    get_seed=get_ints,
    ask=ask_mult,
    correct=correct_mult,
)

game = APIGame(
    "Basic Math Test",
    {
        "addition": AddQ,
        "multiplication": MultQ,
    },
)

game.start(host="localhost", port=8000, root_path="/test")

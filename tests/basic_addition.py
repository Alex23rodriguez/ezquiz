from random import randint

from quizzer import APIGame, Q


def get_ints():
    return randint(1, 10), randint(1, 10)


def ask_addition(t):
    a, b = t
    return f"what is {a} + {b}"


def correct_addition(t):
    return t[0] + t[1]


def explain(t):
    return t


AddQ = Q[tuple[int, int]](
    get_seed=get_ints,
    ask=ask_addition,
    correct=correct_addition,
    explain=explain,
)


game = APIGame("Basic Test", {"test": AddQ})

game.start()

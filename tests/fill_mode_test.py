from random import choice, randint

from ezquiz import APIGame, Q


# Simple fill-in-the-blank questions

# Geography fill questions
geography_questions = {
    "The capital of France is [...].": "Paris",
    "The largest planet in our solar system is [...].": "Jupiter",
    "Water freezes at [...] degrees Celsius.": "0",
    "The chemical symbol for gold is [...].": "Au",
    "Shakespeare wrote [...].": "Hamlet",
}

GeographyQ = Q[str](
    get_seed=lambda: choice(list(geography_questions.keys())),
    ask=lambda seed: seed,
    correct=lambda seed: geography_questions[seed],
    question_type="fill",
)

# Math fill questions
math_fill_questions = {
    "2 + [...] = 5": "3",
    "[...] * 7 = 49": "7",
    "The square root of [...] is 8.": "64",
    "10 - [...] = 3": "7",
    "[...] + 15 = 30": "15",
}

MathFillQ = Q[str](
    get_seed=lambda: choice(list(math_fill_questions.keys())),
    ask=lambda seed: seed,
    correct=lambda seed: math_fill_questions[seed],
    question_type="fill",
)

# Mixed: some simple, some fill
SimpleQ = Q[tuple[int, int]](
    get_seed=lambda: (randint(1, 20), randint(1, 20)),
    ask=lambda t: f"What is {t[0]} + {t[1]}?",
    correct=lambda t: str(t[0] + t[1]),
    question_type="simple",
)

FillMathQ = Q[tuple[int, int]](
    get_seed=lambda: (randint(1, 10), randint(1, 10)),
    ask=lambda t: f"If you have {t[0]} apples and get [...] more, you'll have {t[0] + t[1]} apples.",
    correct=lambda t: str(t[1]),
    question_type="fill",
)

game = APIGame(
    "Fill Mode Test",
    {
        "geography_fill": GeographyQ,
        "math_fill": MathFillQ,
        "simple_addition": SimpleQ,
        "fill_word_problems": FillMathQ,
    },
)

if __name__ == "__main__":
    game.start(host="localhost", port=8001)

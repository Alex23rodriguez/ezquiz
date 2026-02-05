from random import choice

from ezquiz import APIGame, Q

# Misc fill questions using Q.from_dict (returns strings, type="simple" inferred)
MiscQ = Q.from_dict(
    {
        "The capital of France is [...].": "Paris",
        "The largest planet in our solar system is [...].": "Jupiter",
        "Water freezes at [...] degrees Celsius.": "0",
        "The chemical symbol for gold is [...].": "Au",
        "Shakespeare wrote [...].": "Hamlet",
    },
)

# Math fill questions using Q.from_dict
MathFillQ = Q.from_dict(
    {
        "2 + [...] = 5": "3",
        "[...] * 7 = 49": "7",
        "The square root of [...] is 8.": "64",
        "10 - [...] = 3": "7",
        "[...] + 15 = 30": "15",
    },
)

# Fill word problems using Q.from_dict
FillMathQ = Q.from_dict(
    {
        "If you have 3 apples and get [...] more, you'll have 7 apples.": "4",
        "A rectangle has width 5 and length [...], so its area is 35.": "7",
        "The temperature was 20°C, then dropped [...] degrees to reach 12°C.": "8",
    },
)

# Spanish question with context - ask returns a dict
spanish_phrases = [
    ("Mi [...] es John!", "nombre", "My name is John!"),
    ("Hola, ¿cómo [...]?", "estás", "Hello, how are you?"),
    ("Buenos [...]", "días", "Good morning"),
]

SpanishQ = Q[tuple](
    get_seed=lambda: choice(spanish_phrases),
    ask=lambda seed: {
        "text": seed[0],
        "type": "fill",
        "context": seed[2],
    },
    correct=lambda seed: seed[1],
)

# Another example: Math problem with context
math_context_problems = [
    ("[...] + 5 = 12", "7", "Solve for the missing number"),
    ("3 * [...] = 27", "9", "Find the factor"),
]

MathContextQ = Q[tuple](
    get_seed=lambda: choice(math_context_problems),
    ask=lambda seed: {
        "text": seed[0],
        "type": "fill",
        "context": seed[2],
    },
    correct=lambda seed: seed[1],
)

game = APIGame(
    "Fill Mode Test",
    {
        "misc_fill": MiscQ,
        "math_fill": MathFillQ,
        "fill_word_problems": FillMathQ,
        "spanish": SpanishQ,
        "math_context": MathContextQ,
    },
)

if __name__ == "__main__":
    game.start(host="localhost", port=8001)

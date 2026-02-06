from random import choice, randint

from ezquiz import APIGame, Q


# Create first quiz: Basic Math
math_questions = Q.from_dict(
    {
        "What is 2 + 2?": "4",
        "What is 5 + 3?": "8",
        "What is 10 + 5?": "15",
    },
)

# Create second quiz: Geography
geography_questions = Q.from_dict(
    {
        "The capital of France is [...].": "Paris",
        "The largest planet is [...].": "Jupiter",
        "Water freezes at [...]°C.": "0",
    },
    question_type="fill",
)

# Create third quiz: Spanish with context
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

# Create the game and add multiple quizzes
game = APIGame()

game.add_quiz(
    "math",
    "Basic Mathematics",
    {"math": math_questions},
)

game.add_quiz(
    "geography",
    "World Geography",
    {"geo": geography_questions},
)

game.add_quiz(
    "spanish",
    "Spanish Basics",
    {"phrases": SpanishQ},
)

if __name__ == "__main__":
    print("Starting multi-quiz server...")
    print("Visit http://localhost:8000/ to see the lobby")
    print("Available quizzes:")
    print("  - http://localhost:8000/math/")
    print("  - http://localhost:8000/geography/")
    print("  - http://localhost:8000/spanish/")
    game.start(host="localhost", port=8000)

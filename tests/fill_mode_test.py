from ezquiz import APIGame, Q

# Misc fill questions using Q.from_dict
MiscQ = Q.from_dict(
    {
        "The capital of France is [...].": "Paris",
        "The largest planet in our solar system is [...].": "Jupiter",
        "Water freezes at [...] degrees Celsius.": "0",
        "The chemical symbol for gold is [...].": "Au",
        "Shakespeare wrote [...].": "Hamlet",
    },
    question_type="fill",
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
    question_type="fill",
)

# Simple addition using Q.from_dicts with multiple categories
simple_questions = Q.from_dicts(
    [
        {"What is 2 + 2?": "4", "What is 5 + 3?": "8", "What is 10 + 5?": "15"},
        {"What is 3 * 4?": "12", "What is 6 * 7?": "42", "What is 8 * 9?": "72"},
    ],
    ["easy_addition", "easy_multiplication"],
    question_type="simple",
)

# Fill word problems using Q.from_dict
FillMathQ = Q.from_dict(
    {
        "If you have 3 apples and get [...] more, you'll have 7 apples.": "4",
        "A rectangle has width 5 and length [...], so its area is 35.": "7",
        "The temperature was 20°C, then dropped [...] degrees to reach 12°C.": "8",
    },
    question_type="fill",
)

game = APIGame(
    "Fill Mode Test",
    {
        "misc_fill": MiscQ,
        "math_fill": MathFillQ,
        "fill_word_problems": FillMathQ,
        **simple_questions,
    },
)

if __name__ == "__main__":
    game.start(host="localhost", port=8001)

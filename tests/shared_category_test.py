"""
Test to verify that categories with the same name in different quizzes are properly isolated.
This ensures each quiz maintains its own category namespace.
"""

from ezquiz import APIGame, Q

# Quiz 1: Math Basics
math_basics = Q.from_dict(
    {
        "What is 2 + 2?": "4",
        "What is 10 - 5?": "5",
        "What is 3 * 4?": "12",
    },
)

math_advanced = Q.from_dict(
    {
        "What is the square root of 144?": "12",
        "What is 15% of 200?": "30",
    },
)

# Quiz 2: Spanish Basics (same category name "basics")
spanish_basics = Q.from_dict(
    {
        "How do you say 'Hello' in Spanish?": "Hola",
        "How do you say 'Goodbye' in Spanish?": "Adiós",
        "How do you say 'Thank you' in Spanish?": "Gracias",
    },
)

spanish_numbers = Q.from_dict(
    {
        "How do you say '5' in Spanish?": "cinco",
        "How do you say '10' in Spanish?": "diez",
    },
)

# Quiz 3: Geography (also has "basics" category)
geo_basics = Q.from_dict(
    {
        "What is the capital of France?": "Paris",
        "What is the capital of Japan?": "Tokyo",
        "What is the capital of Brazil?": "Brasília",
    },
)

geo_regions = Q.from_dict(
    {
        "Which continent is Egypt in?": "Africa",
        "Which continent is Australia in?": "Australia",
    },
)

# Create the multi-quiz game
game = APIGame()

# All three quizzes have a "basics" category
game.add_quiz(
    "math",
    "Mathematics",
    {
        "basics": math_basics,  # Shared category name
        "advanced": math_advanced,
    },
)

game.add_quiz(
    "spanish",
    "Spanish Language",
    {
        "basics": spanish_basics,  # Same category name, different content
        "numbers": spanish_numbers,
    },
)

game.add_quiz(
    "geography",
    "World Geography",
    {
        "basics": geo_basics,  # Same category name again
        "regions": geo_regions,
    },
)

if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Quiz Test: Shared Category Names")
    print("=" * 60)
    print()
    print("This test verifies that categories with the same name")
    print("in different quizzes are properly isolated.")
    print()
    print("All three quizzes have a 'basics' category:")
    print("  - /math/basics     (Math questions)")
    print("  - /spanish/basics  (Spanish questions)")
    print("  - /geography/basics (Geography questions)")
    print()
    print("Visit http://localhost:8000/ for the lobby")
    print()
    print("=" * 60)
    
    game.start(host="localhost", port=8000)

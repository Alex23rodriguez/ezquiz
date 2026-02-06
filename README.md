# ezquiz

A flexible quiz framework with FastAPI backend and interactive web UI.

## Features

- **Multiple Quiz Support**: Host multiple quizzes under different paths from a single server
- **Custom Logic**: Create custom logic for question generation
- **Quick Start**: Support for simple text input and fill-in-the-blank questions
- **Visual Feedback**: Text diff visualization for incorrect answers
- **Flexible**: Get quizzed only on what is relevant to you

## Installation

```bash
pip install ezquiz
```

## Quick Start

```python
from ezquiz import APIGame, Q

# Create a game
game = APIGame()

# Add a simple quiz using from_dict
questions = Q.from_dict({
    "What is the capital of France?": "Paris",
    "What is the largest planet in the Solar System?": "Jupiter",
})

game.add_quiz("trivia", "General Trivia", {"general": questions})

# Start the server
game.start(host="localhost", port=8000)
```

Visit `http://localhost:8000/` to see the quiz lobby.

## Creating Questions

### Method 1: Using `from_dict` (Simple)

The easiest way to create questions is using `from_dict`, which maps question text to answers:

```python
# Simple text questions
spanish_questions = Q.from_dict({
    "How many eyes does a spider have?": "8",
    "What is the chemical formula for water?": "H2O",
})

# Fill-in-the-blank questions (type="fill")
# Use [...] to indicate where the input field should appear
fill_questions = Q.from_dict(
    {
        "The capital of France is [...].": "Paris",
        "The largest planet in our solar system is [...].": "Jupiter",
        "Water freezes at [...] degrees Celsius.": "0",
    },
    question_type="fill"
)

# Case-sensitive matching (default is case-insensitive)
code_questions = Q.from_dict(
    {"Enter the secret code:": "ABC123"},
    case_sensitive=True
)
```

#### `from_dict` Parameters

- `dct`: Dictionary mapping question strings to answers
- `question_type`: `"simple"` (default) or `"fill"` for inline input
- `case_sensitive`: `False` (default) for case-insensitive matching, `True` for exact case matching

### Method 2: Custom Q with Functions (Flexible)

For more control, create a `Q` instance directly with custom functions. This is useful for:
- Randomized questions
- Dynamic content
- Custom validation logic
- Adding context to questions

```python
from random import randint
from ezquiz import Q

# Create a quiz that generates random addition problems
def get_seed():
    """Generate random numbers for the question."""
    return (randint(1, 20), randint(1, 20))

def ask(seed):
    """Create the question dictionary from the seed."""
    a, b = seed
    return {
        "text": f"What is {a} + {b}?",
        "type": "simple",
        "context": "",  # Optional context shown above question
        "hints": [],    # Optional hints
    }

def correct(seed):
    """Return the correct answer from the seed."""
    a, b = seed
    return str(a + b)

# Create the Q instance
math_q = Q[tuple[int, int]](
    get_seed=get_seed,
    ask=ask,
    correct=correct,
)
```

#### Advanced Example: Spanish with Context

Here's a more complex example with context and multiple question variants:

```python
from random import choice
from ezquiz import Q

# Define phrases with (question, answer, context)
spanish_phrases = [
    ("Mi [...] es John!", "nombre", "My name is John!"),
    ("Hola, ¿cómo [...]?", "estás", "Hello, how are you?"),
    ("Buenos [...]", "días", "Good morning"),
]

spanish_q = Q[tuple](
    get_seed=lambda: choice(spanish_phrases),
    ask=lambda seed: {
        "text": seed[0],           # "Mi [...] es John!"
        "type": "fill",
        "context": seed[2],        # "My name is John!"
    },
    correct=lambda seed: seed[1],  # "nombre"
)
```

## Creating Multi-Quiz Servers

Host multiple quizzes from a single server:

```python
from ezquiz import APIGame, Q

# Create different question sets
math_qs = Q.from_dict({
    "2 + 2 = [...]": "4",
    "5 * 6 = [...]": "30",
}, question_type="fill")

geo_qs = Q.from_dict({
    "Capital of France?": "Paris",
    "Capital of Japan?": "Tokyo",
})

spanish_qs = Q.from_dict({
    "Hello in Spanish?": "Hola",
    "Thank you in Spanish?": "Gracias",
})

# Create game and add quizzes
game = APIGame()

game.add_quiz("math", "Mathematics", {"problems": math_qs})
game.add_quiz("geography", "World Geography", {"capitals": geo_qs})
game.add_quiz("spanish", "Spanish 101", {"vocabulary": spanish_qs})

# Start server
game.start(host="localhost", port=8000)
```

Access:
- Lobby: `http://localhost:8000/`
- Math: `http://localhost:8000/math/`
- Geography: `http://localhost:8000/geography/`
- Spanish: `http://localhost:8000/spanish/`

## Question Types

### Simple Questions
Text input field below the question:

```python
Q.from_dict({"What is 2+2?": "4"}, question_type="simple")
```

### Fill-in-the-Blank
Inline input field within the text:

```python
Q.from_dict(
    {"The capital of [...] is Paris.": "France"},
    question_type="fill"
)
```

## Answer Validation

### Case-Insensitive (Default)

```python
Q.from_dict({"What color is the sky?": "blue"})
# Accepts: "blue", "Blue", "BLUE", etc.
```

### Case-Sensitive

```python
Q.from_dict(
    {"Enter the code:": "AbC123"},
    case_sensitive=True
)
# Only accepts: "AbC123"
```

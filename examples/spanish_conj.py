from random import choice

from ezquiz import APIGame, Q

# Regular Spanish verbs by ending
verbs_ar = ["hablar", "comprar", "estudiar", "trabajar"]
verbs_er = ["comer", "beber", "leer", "aprender"]
verbs_ir = ["vivir", "escribir", "abrir", "recibir"]

# Subject pronouns and their conjugation endings
subjects = [
    ("Yo", {"ar": "o", "er": "o", "ir": "o"}),
    ("Tú", {"ar": "as", "er": "es", "ir": "es"}),
    ("Él/Ella", {"ar": "a", "er": "e", "ir": "e"}),
    ("Nosotros", {"ar": "amos", "er": "emos", "ir": "imos"}),
    ("Ellos", {"ar": "an", "er": "en", "ir": "en"}),
]


def get_seed():
    """Randomly select a subject and verb."""
    verb = choice(verbs_ar + verbs_er + verbs_ir)
    subject = choice(subjects)
    return (verb, subject)


def ask(seed):
    """Create a conjugation question."""
    verb, (subject, _) = seed
    return {
        "text": f"{subject} [...] ({verb})",
        "type": "fill",
        "context": f"Conjugate the verb '{verb}' for '{subject}'",
    }


def correct(seed):
    """Return the correctly conjugated verb."""
    verb, (subject, endings) = seed
    # Get the verb stem (remove -ar/-er/-ir)
    stem = verb[:-2]
    # Get the ending based on the verb type
    ending = verb[-2:]  # "ar", "er", or "ir"
    return stem + endings[ending]


# Create the conjugation quiz
spanish_verbs_q = Q[tuple](
    get_seed=get_seed,
    ask=ask,
    correct=correct,
)

# create server
if __name__ == "__main__":
    game = APIGame()
    game.add_quiz(
        subpath="spanish", title="Spanish verbs", qs={"regular verbs": spanish_verbs_q}
    )
    game.start(host="localhost", port=8000)

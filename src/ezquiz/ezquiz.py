"""ezquiz - A flexible quiz framework with FastAPI backend and interactive web UI.

This module provides the Q class for defining quiz questions with various input types
and validation strategies.

Example:
    >>> from ezquiz import Q
    >>>
    >>> # Simple text question using from_dict
    >>> math_q = Q.from_dict({
    ...     "What is 2 + 2?": "4",
    ...     "What is 5 + 3?": "8",
    ... })
    >>>
    >>> # Fill-in-the-blank question
    >>> fill_q = Q.from_dict(
    ...     {"The capital of France is [...].": "Paris"},
    ...     question_type="fill"
    ... )
    >>>
    >>> # Complex question with context
    >>> spanish_q = Q[str](
    ...     get_seed=lambda: ("Mi [...] es John!", "nombre", "My name is John!"),
    ...     ask=lambda seed: {
    ...         "text": seed[0],
    ...         "type": "fill",
    ...         "context": seed[2],
    ...     },
    ...     correct=lambda seed: seed[1],
    ... )
"""

from random import choice
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class Q(Generic[T]):
    """A generic question template for creating quiz questions.

    The Q class provides a flexible framework for defining questions with
    customizable question generation, answer validation, and explanations.

    Type Parameters:
        T: The type of the seed/object used to generate questions.

    Attributes:
        get_seed: Function that returns a seed of type T for question generation.
        ask: Function that takes a seed and returns a question dict with keys:
             - text: The question text
             - type: "simple" or "fill"
             - context: Optional context/instructions
             - hints: List of hints (optional)
        correct: Function that takes a seed and returns the correct answer.
        check: Function that validates submitted answers against correct answers.
        explain: Function that provides explanation for incorrect answers.

    Example:
        >>> # Simple math question
        >>> math_q = Q[tuple[int, int]](
        ...     get_seed=lambda: (randint(1, 10), randint(1, 10)),
        ...     ask=lambda t: {"text": f"What is {t[0]} + {t[1]}?", "type": "simple"},
        ...     correct=lambda t: str(t[0] + t[1]),
        ... )
    """

    def __init__(
        self,
        get_seed: Callable[[], T],
        ask: Callable[[T], dict],
        correct: Callable[[T], str],
        check: Callable[[T, str], bool] | None = None,
        explain: Callable[[T], dict] | None = None,
    ):
        """Initialize a Question template.

        Args:
            get_seed: Function that returns a seed for question generation.
            ask: Function that converts seed to question dict.
            correct: Function that returns correct answer from seed.
            check: Optional custom validation function. Defaults to string equality.
            explain: Optional function returning explanation dict with type and value.
        """
        self.get_seed = get_seed
        self.ask = ask
        self.correct = correct

        if check is None:
            self.check = (
                lambda correct_ans, submitted_ans: str(correct_ans) == submitted_ans
            )
        else:
            self.check = check

        if explain is None:
            self.explain = lambda _: {"type": "text_diff"}

        else:
            self.explain = explain

    @classmethod
    def from_dict(
        cls,
        dct: dict,
        question_type: str = "simple",
        case_sensitive: bool = False,
        **kwargs,
    ):
        """Create a Q instance from a dictionary of questions and answers.

        This is a convenience method for simple use cases where questions are
        static strings mapped to their answers.

        Args:
            dct: Dictionary mapping question strings to their correct answers.
            question_type: Type of question input - "simple" (text field) or
                          "fill" (inline input in text).
            case_sensitive: Whether answer comparison is case-sensitive.
                          Defaults to False (case-insensitive).
            **kwargs: Additional arguments passed to Q constructor.

        Returns:
            Q instance configured with the provided dictionary.

        Example:
            >>> # Simple questions (case-insensitive by default)
            >>> q = Q.from_dict({
            ...     "What is 2 + 2?": "4",
            ...     "What is the capital of France?": "Paris",
            ... })
            >>>
            >>> # Fill-in-the-blank questions
            >>> q = Q.from_dict(
            ...     {"The chemical symbol for gold is [...].": "Au"},
            ...     question_type="fill"
            ... )
            >>>
            >>> # Case-sensitive matching
            >>> q = Q.from_dict(
            ...     {"Enter the secret code:": "ABC123"},
            ...     case_sensitive=True
            ... )
        """

        def make_check():
            if case_sensitive:
                return (
                    lambda correct_ans, submitted_ans: str(correct_ans) == submitted_ans
                )
            else:
                return (
                    lambda correct_ans, submitted_ans: str(correct_ans).lower()
                    == submitted_ans.lower()
                )

        return cls(
            get_seed=lambda: choice(list(dct.keys())),
            ask=lambda seed: {
                "text": str(seed),
                "type": question_type,
                "context": "",
                "hints": [],
            },
            correct=lambda seed: dct[seed],
            check=make_check(),
            **kwargs,
        )

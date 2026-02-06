from random import choice
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class Q(Generic[T]):
    def __init__(
        self,
        get_seed: Callable[[], T],
        ask: Callable[[T], dict],
        correct: Callable[[T], str],
        check: Callable[[T, str], bool] | None = None,
        explain: Callable[[T], dict] | None = None,
    ):
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
            self.explain = lambda _: "{textdiff}"

        else:
            self.explain = explain

    @classmethod
    def from_dict(cls, dct: dict, question_type: str = "simple", **kwargs):
        return cls(
            get_seed=lambda: choice(list(dct.keys())),
            ask=lambda seed: {
                "text": str(seed),
                "type": question_type,
                "context": "",
                "hints": [],
            },
            correct=lambda seed: dct[seed],
            **kwargs,
        )

from random import choice
from typing import Callable, Generic, Literal, TypedDict, TypeVar

T = TypeVar("T")

Prompt = TypedDict("Prompt", {"type": Literal["text", "audio"], "value": str})

Explain = TypedDict("Explain", {"type": Literal["text", "text_diff"], "value": str})


class Q(Generic[T]):
    def __init__(
        self,
        get_seed: Callable[[], T],
        ask: Callable[[T], str],
        correct: Callable[[T], str],
        check: Callable[[T, str], bool] | None = None,
        explain: Callable[[T], Explain] | None = None,
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
    def from_dict(cls, dct: dict):
        return cls(
            get_seed=lambda: choice(dct),
            ask=lambda seed: str(seed),
            correct=lambda seed: dct[seed],
        )

    @classmethod
    def from_dicts(cls, dcts: list[dict], names: list, include_reverse=False):
        assert len(dcts) == len(names)
        qs = {name: cls.from_dict(d) for name, d in zip(names, dcts)}

        if include_reverse:
            for name, d in zip(names, dcts):
                qs[name] = cls.from_dict({val: key for key, val in d.items()})

        return qs

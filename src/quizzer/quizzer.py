from typing import Callable, Generic, Literal, TypedDict, TypeVar

T = TypeVar("T")

Prompt = TypedDict("Prompt", {"type": Literal["text", "audio"], "value": str})

Explain = TypedDict("Explain", {"type": Literal["text", "text_diff"], "value": str})


class Q(Generic[T]):
    def __init__(
        self,
        get_seed: Callable[[], T],
        ask: Callable[[T], str],
        check: Callable[[T, str], bool],
        explain: Callable[[T], Explain] | None,
    ):
        self.get_seed = get_seed
        self.ask = ask
        self.check = check
        self.explain = explain

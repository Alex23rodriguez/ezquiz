from typing import Literal


class CLIGame:
    def __init__(self) -> None:
        self.score = 0
        self.mistakes = 0
        self.streak = 0
        self.history = []

    def start(
        self,
        mode: Literal["timed", "score", "mistakes", "total", "streak"] = "score",
        param=10,
    ):
        pass

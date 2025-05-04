"""
RPi
"""
from typing import Literal

class PiPin:
    "A Raspberry Pi GPIO Pin"

    def __init__(
        self,
        bcm: int,
        board: int = -1,
        name: str = "",
        mode: Literal["IN", "OUT"] = "IN",
        state: str | None = None,
        description: str | None = None,
        usage: str | None = None
    ):
        self.bcm = bcm
        self.board = board
        self.name = name
        self.mode: str = mode.upper() if mode else "IN"
        self.state: str | None = state
        self.description: str | None = description
        self.usage: str | None = usage

        if self.mode not in ["IN", "OUT"]:
            raise ValueError(f"Invalid mode: {self.mode}")

    @property
    def is_input(self):
        return self.mode == "IN"

    @property
    def is_output(self):
        return self.mode == "OUT"

    def __repr__(self):
        return f"<PiPin {self.name} (BCM {self.bcm}, BOARD {self.board}) Mode={self.mode}, State={self.state}>"

    def __str__(self):
        return f"<PiPin {self.name} (BCM {self.bcm}, BOARD {self.board}) Mode={self.mode}, State={self.state}>"

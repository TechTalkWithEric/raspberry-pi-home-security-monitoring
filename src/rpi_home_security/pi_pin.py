"""
RPi
"""
class PiPin:
    def __init__(self, bcm, board, name):
        self.bcm = bcm
        self.board = board
        self.name = name
        self.mode = None
        self.state = None

    @property
    def is_input(self):
        return self.mode == "IN"

    @property
    def is_output(self):
        return self.mode == "OUT"

    def __repr__(self):
        return f"<PiPin {self.name} (BCM {self.bcm}, BOARD {self.board}) Mode={self.mode}, State={self.state}>"

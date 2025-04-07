from datetime import datetime

class SecurityInput:
    def __init__(self, name: str):
        self.name: str = name
        self.location: str | None = None
        self.type: str | None = None # motion, door, window, etc.
        self.state: str | None = None # open, closed, motion, etc.
        self.last_updated: datetime = datetime.now()
        self.pin: int | None = None
        self.zone: str | None = None
class SecurityInputs:
    pass    
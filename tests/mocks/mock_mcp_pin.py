"""
"""

class MockMcpPin:
    """
    A mock pin class to simulate the behavior of a MCP23017 pin.
    """
   
    def __init__(self, pin_number, initial_value=True):
        self.pin_number = pin_number
        self.value = initial_value
        self.direction = None
        self.pull = None

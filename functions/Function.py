"""Class to hold a function"""

class Function():
    def __init__(self, name = "f", value = "x"):
        self._name = name
        self._value = value

    def display(self):
        print(f"{self.name}(x) = {self._value}")
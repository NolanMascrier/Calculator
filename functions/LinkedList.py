class LList():
    def __init__(self, data, operator):
        self._data = data
        self._operator = operator
        self._next = None
    
    def push(self, data):
        if self._next is None:
            self._next = data
        else:
            self._next.push(data)

    def __str__(self):
        return self._data + ", " + self._operator + (" -> " + str(self._next)) if self._next is not None else ""
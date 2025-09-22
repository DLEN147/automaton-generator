class State:
    def __init__(self, name, is_accepting=False):
        self.name = name
        self.is_accepting = is_accepting

    def __repr__(self):
        return f"State({self.name}, accepting={self.is_accepting})"

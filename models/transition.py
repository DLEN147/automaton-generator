class Transition:
    def __init__(self, current_state, symbol, next_state):
        self.current_state = current_state
        self.symbol = symbol
        self.next_state = next_state

    def __repr__(self):
        return f"δ({self.current_state}, '{self.symbol}') → {self.next_state}"

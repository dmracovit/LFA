import random

class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN  # NT
        self.VT = VT  # T
        self.P = P  # production rule
        self.S = S  # start symbol

    def generate_string(self):
        """Generate a valid string based on the grammar rules."""
        current = [self.S]
        while any(symbol in self.VN for symbol in current):  #replacing non-terminals
            for i, symbol in enumerate(current):
                if symbol in self.VN:  #replace first non-terminal
                    production = random.choice(self.P[symbol])
                    current = current[:i] + list(production) + current[i + 1:]
                    break 
        return ''.join(current)

    def to_finite_automaton(self):
        """Convert the grammar to a finite automaton."""
        states = set(self.VN) | {'F'}  #final state
        alphabet = set(self.VT)
        start_state = self.S
        accept_states = {'F'}
        transitions = {state: {} for state in states}

        for nt, productions in self.P.items():
            for production in productions:
                if len(production) == 1:  # A → a (transition to final)
                    transitions[nt][production[0]] = 'F'
                else:  # A → aB (transition to another state)
                    first_symbol = production[0]
                    next_state = production[1]
                    transitions[nt][first_symbol] = next_state

        return FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)


class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def string_belongs_to_language(self, input_string):
        """Check if a given string is accepted by the finite automaton."""
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False  
            if symbol not in self.transitions[current_state]:
                return False  
            current_state = self.transitions[current_state][symbol]
        return current_state in self.accept_states


if __name__ == "__main__":
    VN = {'S', 'A', 'B', 'C'}
    VT = {'a', 'b', 'c', 'd'}
    P = {
        'S': ['dA'],
        'A': ['aB', 'b'],
        'B': ['bC', 'd'],
        'C': ['cB', 'aA']
    }
    S = 'S'

    grammar = Grammar(VN, VT, P, S)

    print("\nGenerated Strings:")
    for _ in range(5):
        print(grammar.generate_string())

    fa = grammar.to_finite_automaton()

    test_strings = ['d', 'db', 'baad', '']
    print("\nString Belonging to Language:")
    for s in test_strings:
        print(f"'{s}' -> {fa.string_belongs_to_language(s)}")

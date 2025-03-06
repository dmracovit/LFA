import random
from collections import defaultdict
from graphviz import Digraph


class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN  # Non-terminals
        self.VT = VT  # Terminals
        self.P = P  # Production rules
        self.S = S  # Start symbol

    def generate_string(self):
        """Generate a valid string based on the grammar rules."""
        current = [self.S]
        while any(symbol in self.VN for symbol in current):  # Replace non-terminals
            for i, symbol in enumerate(current):
                if symbol in self.VN:  # Replace first non-terminal
                    production = random.choice(self.P[symbol])
                    current = current[:i] + list(production) + current[i + 1:]
                    break
        return ''.join(current)

    def classify_grammar(self):
        """Classify the grammar based on the Chomsky hierarchy."""
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for lhs, productions in self.P.items():
            for production in productions:
                # Check for Regular Grammar (Type 3)
                if len(production) == 1 and production[0] in self.VT:
                    continue
                elif len(production) == 2 and production[0] in self.VT and production[1] in self.VN:
                    continue
                else:
                    is_regular = False

                # Check for Context-Free Grammar (Type 2)
                if len(lhs) != 1 or lhs not in self.VN:
                    is_context_free = False

                # Check for Context-Sensitive Grammar (Type 1)
                if len(production) < len(lhs):
                    is_context_sensitive = False

        if is_regular:
            return "Type 3 (Regular)"
        elif is_context_free:
            return "Type 2 (Context-Free)"
        elif is_context_sensitive:
            return "Type 1 (Context-Sensitive)"
        else:
            return "Type 0 (Unrestricted)"

    def to_finite_automaton(self):
        """Convert the grammar to a finite automaton."""
        states = set(self.VN) | {'F'}  # Final state
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

    def is_deterministic(self):
        """Check if the finite automaton is deterministic."""
        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                if isinstance(next_state, set):
                    return False
        return True

    def convert_ndfa_to_dfa(self):
        """Convert an NDFA to a DFA using subset construction."""
        dfa_states = set()
        dfa_transitions = defaultdict(dict)
        dfa_start_state = frozenset({self.start_state})
        dfa_accept_states = set()

        stack = [dfa_start_state]
        dfa_states.add(dfa_start_state)

        while stack:
            current_state = stack.pop()

            for symbol in self.alphabet:
                next_state = frozenset(
                    {next_state for state in current_state for next_state in self.transitions[state].get(symbol, set())}
                )

                if next_state:
                    dfa_transitions[current_state][symbol] = next_state

                    if next_state not in dfa_states:
                        dfa_states.add(next_state)
                        stack.append(next_state)

                    if any(state in self.accept_states for state in next_state):
                        dfa_accept_states.add(next_state)

        return FiniteAutomaton(dfa_states, self.alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)

    def to_regular_grammar(self):
        """Convert the finite automaton to a regular grammar."""
        VN = self.states
        VT = self.alphabet
        P = {}
        S = self.start_state

        for state, transitions in self.transitions.items():
            P[state] = []
            for symbol, next_state in transitions.items():
                if next_state in self.accept_states:
                    P[state].append(symbol)
                else:
                    P[state].append(symbol + next_state)

        return Grammar(VN, VT, P, S)

    def visualize(self):
        """Visualize the finite automaton using graphviz."""
        dot = Digraph()

        for state in self.states:
            if state in self.accept_states:
                dot.node(str(state), shape='doublecircle')
            else:
                dot.node(str(state))

        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                dot.edge(str(state), str(next_state), label=symbol)

        dot.render('finite_automaton', format='png', cleanup=True)
        return dot


if __name__ == "__main__":
    # Define the finite automaton for Variant 26
    states = {'q0', 'q1', 'q2', 'q3'}
    alphabet = {'a', 'b', 'c'}
    transitions = {
        'q0': {'a': {'q0', 'q1'}},  # Non-deterministic transition
        'q1': {'b': {'q1'}, 'a': {'q2'}},
        'q2': {'c': {'q3'}},
        'q3': {'c': {'q3'}}
    }
    start_state = 'q0'
    accept_states = {'q3'}

    # Create the finite automaton
    fa = FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)

    # Check if the FA is deterministic
    print("\nIs FA Deterministic?")
    print(fa.is_deterministic())  # Expected: False (since δ(q0, a) has two possible states)

    # Convert NDFA to DFA
    print("\nConvert NDFA to DFA:")
    dfa = fa.convert_ndfa_to_dfa()
    print("DFA States:", dfa.states)
    print("DFA Transitions:", dfa.transitions)
    print("DFA Start State:", dfa.start_state)
    print("DFA Accept States:", dfa.accept_states)

    # Convert FA to Regular Grammar
    print("\nConvert FA to Regular Grammar:")
    regular_grammar = fa.to_regular_grammar()
    print("VN:", regular_grammar.VN)
    print("VT:", regular_grammar.VT)
    print("P:", regular_grammar.P)
    print("S:", regular_grammar.S)

    # Visualize the FA (optional)
    print("\nVisualize FA:")
    fa.visualize()
import random
from graphviz import Digraph

class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN  # Non-terminals
        self.VT = VT  # Terminals
        self.P = P    # Productions
        self.S = S    # Start symbol

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
                    transitions[nt][production[0]] = {'F'}
                else:  # A → aB (transition to another state)
                    first_symbol = production[0]
                    next_state = production[1]
                    if first_symbol not in transitions[nt]:
                        transitions[nt][first_symbol] = set()
                    transitions[nt][first_symbol].add(next_state)

        return FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)

    def classify_grammar(self):
        """Classify the grammar based on Chomsky hierarchy."""
        is_type_3 = True
        for lhs in self.P:
            if len(lhs) != 1 or lhs not in self.VN:
                return "Type 0 (Unrestricted)"
            for production in self.P[lhs]:
                if len(production) == 0:
                    if lhs != self.S:
                        is_type_3 = False
                    continue
                if len(production) == 1:
                    if production[0] not in self.VT:
                        is_type_3 = False
                else:
                    terminals = 0
                    non_terminals = 0
                    for char in production:
                        if char in self.VT:
                            terminals += 1
                        elif char in self.VN:
                            non_terminals += 1
                    if non_terminals != 1 or terminals != len(production) - 1:
                        is_type_3 = False
                    if production[-1] not in self.VN and production[0] not in self.VN:
                        is_type_3 = False
        return "Type 3 (Regular)" if is_type_3 else "Type 2 (Context-free)"

    def __repr__(self):
        """Pretty-print the grammar in the desired format."""
        return f"""Grammar {{
  VN: {sorted(list(self.VN))},
  VT: {sorted(list(self.VT))},
  startVariable: '{self.S}',
  hashMap: {{
    {',\n    '.join(f"'{k}' => {v}" for k, v in sorted(self.P.items()))}
  }}
}}"""


class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def string_belongs_to_language(self, input_string):
        """Check if a string is accepted by the automaton."""
        current_states = {self.start_state}
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                next_states.update(self.transitions.get(state, {}).get(symbol, set()))
            current_states = next_states
            if not current_states:
                return False
        return any(state in self.accept_states for state in current_states)

    def is_deterministic(self):
        """Check if the automaton is deterministic."""
        for state in self.transitions:
            for symbol in self.transitions[state]:
                # multiple transitions for the same symbol
                if len(self.transitions[state][symbol]) > 1:
                    return False
                # epsilon transitions (non-deterministic)
                if symbol == '':
                    return False
            # if all symbols in the alphabet are defined for the state
            for symbol in self.alphabet:
                if symbol not in self.transitions[state]:
                    return False
        return True

    def to_regular_grammar(self):
        """Convert the automaton to a regular grammar."""
        P = {state: [] for state in self.states}
        for state in self.transitions:
            for symbol in self.transitions[state]:
                for next_state in self.transitions[state][symbol]:
                    P[state].append(f"{symbol}{next_state}")
        for accept in self.accept_states:
            P[accept].append('')
        return Grammar(self.states, self.alphabet, P, self.start_state)

    def convert_to_dfa(self):
        """Convert NFA to DFA using subset construction."""
        dfa_start = frozenset({self.start_state})
        dfa_states = {dfa_start}
        dfa_accept = set()
        dfa_transitions = {}
        queue = [dfa_start]

        # Map frozenset states to readable names (q0, q1, etc.)
        state_names = {dfa_start: 'q0'}
        state_counter = 1

        if any(state in self.accept_states for state in dfa_start):
            dfa_accept.add(state_names[dfa_start])

        while queue:
            current = queue.pop(0)
            current_name = state_names[current]
            dfa_transitions[current_name] = {}

            for symbol in self.alphabet:
                next_states = set()
                for state in current:
                    if symbol in self.transitions.get(state, {}):
                        next_states.update(self.transitions[state][symbol])
                next_frozen = frozenset(next_states)

                if not next_frozen: 
                    continue

                if next_frozen not in state_names:
                    state_names[next_frozen] = f'q{state_counter}'
                    state_counter += 1
                    queue.append(next_frozen)
                    if any(state in self.accept_states for state in next_frozen):
                        dfa_accept.add(state_names[next_frozen])

                dfa_transitions[current_name][symbol] = state_names[next_frozen]

        dfa_states_renamed = set(state_names.values())
        return FiniteAutomaton(
            dfa_states_renamed,
            self.alphabet,
            dfa_transitions,
            state_names[dfa_start],
            dfa_accept
        )

    def visualize(self, title="FA"):
        """Generate a visual representation of the automaton."""
        dot = Digraph(comment=title)
        dot.attr(rankdir='LR')
        dot.node('start', shape='none', label='')
        dot.edge('start', self.start_state)
        for state in self.states:
            if state in self.accept_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')
            for symbol, next_states in self.transitions[state].items():
                for next_state in next_states:
                    dot.edge(state, next_state, label=symbol)
        dot.render(title, format='png', cleanup=True)
        print(f"Visualization saved as {title}.png")

    def __repr__(self):
        """Pretty-print the automaton in the desired format."""
        return f"""Q: {{{', '.join(map(str, self.states))}}}
Sigma: {{{', '.join(self.alphabet)}}}
delta: {self._format_transitions()}
q0: {self.start_state}
F: {{{', '.join(map(str, self.accept_states))}}}"""

    def _format_transitions(self):
        """Format transitions for pretty-printing."""
        transitions = []
        for state in self.transitions:
            for symbol in self.transitions[state]:
                for next_state in self.transitions[state][symbol]:
                    transitions.append(f'["{state},{symbol}","{next_state}"]')
        return f"[{', '.join(transitions)}]"


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

    variant_states = {'q0', 'q1', 'q2', 'q3'}
    variant_alphabet = {'a', 'b', 'c'}
    variant_transitions = {
        'q0': {'a': {'q0', 'q1'}},
        'q1': {'b': {'q1'}, 'a': {'q2'}},
        'q2': {'c': {'q3'}},
        'q3': {'c': {'q3'}}
    }
    variant_start = 'q0'
    variant_accept = {'q3'}

    variant_dfa = FiniteAutomaton(
        variant_states,
        variant_alphabet,
        variant_transitions,
        variant_start,
        variant_accept
    )

    generated_string = grammar.generate_string()
    print(f"Generated string: {generated_string}")

    print(f"Grammar classification: {grammar.classify_grammar()}")

    fa = grammar.to_finite_automaton()
    print("\nFinite Automaton:")
    print(fa)

    print("\nIs deterministic:", fa.is_deterministic())

    dfa = fa.convert_to_dfa()
    print("\nDFA:")
    print(dfa)

    print("\nRegular Grammar:")
    print(grammar)

    fa.visualize("NDFA")
    variant_dfa.visualize("DFA")
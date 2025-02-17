# Laboratory work 1

### Course: Formal Languages & Finite Automata
### Author: Racovita Dumitru

----

## Theory
If needed, but it should be written by the author in her/his words.


## Objectives:

   1.Discover what a language is and what it needs to have in order to be considered a formal one;

  2.Provide the initial setup for the evolving project that you will work on during this semester. You can deal with each laboratory work as a separate task or project to demonstrate your understanding of the given themes, but you also can deal with labs as stages of making your own big solution, your own project. Do the following:

   a. Create GitHub repository to deal with storing and updating your project;

  b. Choose a programming language. Pick one that will be easiest for dealing with your tasks, you need to learn how to solve the problem itself, not everything around the problem (like setting up the project, launching it correctly and etc.);

  c. Store reports separately in a way to make verification of your work simpler (duh)

   3.According to your variant number, get the grammar definition and do the following:

  a. Implement a type/class for your grammar;

  b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

  c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

   d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;


## Implementation description

* Grammar Class:

    Defines a formal grammar with non-terminals (VN), terminals (VT), production rules (P), and a start symbol (S).
    generate_string(): Randomly builds a valid string by replacing non-terminals using production rules until only terminals remain.
    to_finite_automaton(): Converts the grammar into a finite automaton by defining states, transitions, and final states.

* FiniteAutomaton Class:

    Represents a state machine with states, alphabet, transitions, start state, and final states.
    string_belongs_to_language(): Checks if an input string follows valid state transitions, verifying if it belongs to the language.

* Main Execution:

    Creates a grammar, generates 5 sample strings, and converts it into an automaton.
    Tests different input strings to check if they belong to the language.


python
```
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

    test_strings = ['da']
    print("\nString Belonging to Language:")
    for s in test_strings:
        print(f"'{s}' -> {fa.string_belongs_to_language(s)}")

```

* ![image](https://github.com/user-attachments/assets/0ef2876b-6914-414e-9584-fc2026665b6b)



## Conclusions 
   This laboratory work introduced formal grammars and finite automata, showing how to define a language using production rules and convert it into a state machine. The implementation generates valid strings and verifies if an input belongs to the language. This demonstrates the connection between regular grammars and finite automata, reinforcing their role in computational theory and language processing.


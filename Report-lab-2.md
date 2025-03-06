
# Laboratory Work 2

### Course: Formal Languages & Finite Automata  
### Author: Cretu Dumitru  
### Kudos to Vasile Drumea and Irina Cojuhari  

---

## Theory

Formal languages and finite automata are fundamental concepts in computer science, particularly in the study of computational theory, compiler design, and language processing. A **formal language** is a set of strings composed of symbols from a specified alphabet, constructed according to a set of rules defined by a grammar. These rules, known as **production rules**, dictate how symbols can be combined to form valid strings within the language.

A **grammar** is formally defined as a quadruple \( G = (V_N, V_T, P, S) \), where:
- \( V_N \) is a set of non-terminal symbols (variables that can be replaced by other symbols).
- \( V_T \) is a set of terminal symbols (the alphabet of the language).
- \( P \) is a set of production rules that describe how non-terminals can be replaced by combinations of terminals and non-terminals.
- \( S \) is the start symbol, from which all valid strings in the language are derived.

A **finite automaton (FA)** is a mathematical model used to recognize patterns within input strings. It consists of:
- A finite number of **states**.
- **Transitions** between these states based on input symbols.
- A **start state**.
- One or more **accept (or final) states**.

Finite automata are closely related to regular grammars, as every regular grammar can be converted into a finite automaton and vice versa. This laboratory work explores the relationship between grammars and finite automata, focusing on **determinism**, **non-determinism**, and the **Chomsky hierarchy**.

---

## Objectives

The primary objectives of this laboratory work are:
1. **Understand the concept of finite automata** and their classification into deterministic (DFA) and non-deterministic (NDFA) automata.
2. **Implement conversion from NDFA to DFA** using the subset construction algorithm.
3. **Classify a grammar** based on the Chomsky hierarchy.
4. **Convert a finite automaton to a regular grammar**.
5. **Represent the finite automaton graphically** (optional).

---

## Implementation

The implementation is divided into two main components: the **Grammar class** and the **FiniteAutomaton class**. Below is a description of the key functionalities and methods.

### Grammar Class

The `Grammar` class represents a formal grammar with attributes for non-terminals (\( V_N \)), terminals (\( V_T \)), production rules (\( P \)), and the start symbol (\( S \)).

#### Key Methods:
1. **`generate_string`**:
   - Generates a valid string by iteratively replacing non-terminal symbols with their corresponding productions until only terminal symbols remain.
   - Starts with the start symbol \( S \) and uses random selection to choose among possible productions for each non-terminal.

2. **`classify_grammar`**:
   - Classifies the grammar based on the Chomsky hierarchy (Type 0, 1, 2, or 3).
   - Checks the structure of production rules to determine the grammar type.

3. **`to_finite_automaton`**:
   - Converts the grammar into a finite automaton.
   - Defines states as non-terminals plus an additional final state \( F \).
   - Creates transitions based on the production rules.

### FiniteAutomaton Class

The `FiniteAutomaton` class represents a finite automaton with attributes for states, alphabet, transitions, start state, and accept states.

#### Key Methods:
1. **`string_belongs_to_language`**:
   - Checks if a given input string is accepted by the automaton.
   - Simulates the automaton's operation by following transitions for each symbol in the input string.

2. **`is_deterministic`**:
   - Determines if the automaton is deterministic by checking for multiple transitions for the same input symbol.

3. **`convert_ndfa_to_dfa`**:
   - Converts a non-deterministic finite automaton (NDFA) to a deterministic finite automaton (DFA) using the subset construction algorithm.

4. **`to_regular_grammar`**:
   - Converts the finite automaton into a regular grammar.

5. **`visualize`**:
   - Generates a graphical representation of the finite automaton using the `graphviz` library.

---

## Main Execution

The program is executed using a predefined finite automaton for **Variant 26**:
- **States (Q):** `{q0, q1, q2, q3}`
- **Alphabet (∑):** `{a, b, c}`
- **Final States (F):** `{q3}`
- **Transitions (δ):**
  - `δ(q0, a) = q1`
  - `δ(q1, b) = q1`
  - `δ(q1, a) = q2`
  - `δ(q0, a) = q0`
  - `δ(q2, c) = q3`
  - `δ(q3, c) = q3`

### Code Snippet:
```python
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
```
## Results

  Is FA Deterministic?

  Output: False (since δ(q0, a) has two possible states, q0 and q1).
    Convert NDFA to DFA:

  The DFA states, transitions, start state, and accept states are printed.

Convert FA to Regular Grammar:

  The resulting grammar's non-terminals (VNVN​), terminals (VTVT​), production rules (PP), and start symbol (SS) are printed.
  Visualize FA:

   A graphical representation of the FA is saved as finite_automaton.png.

## Conclusions

This laboratory work provided a practical exploration of finite automata, focusing on determinism, non-determinism, and the Chomsky hierarchy. By implementing a finite automaton and performing conversions between NDFA and DFA, we demonstrated the close relationship between these models and their applications in language processing.

The project also emphasized the importance of structured implementation and clear documentation. Future work could explore more complex grammars, such as context-free grammars, and their corresponding automata, as well as applications in parsing and compiler design.

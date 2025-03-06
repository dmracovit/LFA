# Laboratory work 1.

### Course: Formal Languages & Finite Automata
### Author: Racovita Dumitru

----
Theory

Formal languages and finite automata are foundational concepts in computer science, particularly in the study of computational theory and compiler design. A formal language is a set of strings composed of symbols from a specified alphabet, constructed according to a set of rules defined by a grammar. These rules, known as production rules, dictate how symbols can be combined to form valid strings within the language.

A grammar is formally defined as a quadruple G=(VN,VT,P,S)G=(VN​,VT​,P,S), where:

    VNVN​ is a set of non-terminal symbols (variables that can be replaced by other symbols).

    VTVT​ is a set of terminal symbols (the alphabet of the language).

    PP is a set of production rules that describe how non-terminals can be replaced by combinations of terminals and non-terminals.

    SS is the start symbol, from which all valid strings in the language are derived.

A finite automaton (FA) is a mathematical model used to recognize patterns within input strings. It consists of a finite number of states, transitions between these states based on input symbols, a start state, and one or more accept (or final) states. Finite automata are closely related to regular grammars, as every regular grammar can be converted into a finite automaton and vice versa.

The connection between grammars and finite automata is crucial in understanding how languages are defined and processed. This laboratory work explores this relationship by implementing a grammar, generating valid strings, and converting the grammar into a finite automaton to verify the validity of input strings.
Objectives

The primary objectives of this laboratory work are:

    To understand the concept of formal languages and the components required to define them.

    To set up a project structure for implementing and evolving solutions related to formal languages and finite automata. This includes:

        Creating a GitHub repository for version control and collaboration.

        Selecting a programming language suitable for the tasks.

        Organizing reports and code for ease of verification.

    To implement a grammar based on a given variant and perform the following tasks:

        Define a class to represent the grammar.

        Generate valid strings from the language defined by the grammar.

        Convert the grammar into a finite automaton.

        Implement functionality to check if an input string belongs to the language recognized by the finite automaton.

Implementation

The implementation is divided into two main components: the Grammar class and the FiniteAutomaton class. Below is a description of the key functionalities and methods:
Grammar Class

The Grammar class represents a formal grammar with attributes for non-terminals (VN), terminals (VT), production rules (P), and the start symbol (S).
Key Methods:

    generate_string:

        This method generates a valid string by iteratively replacing non-terminal symbols with their corresponding productions until only terminal symbols remain.

        It starts with the start symbol S and uses random selection to choose among possible productions for each non-terminal.

        The process continues until no non-terminals are left in the string.

    to_finite_automaton:

        This method converts the grammar into a finite automaton.

        It defines the states as the non-terminals plus an additional final state F.

        Transitions are created based on the production rules. For example, a rule like A→aBA→aB results in a transition from state AA to state BB on input symbol aa.

        The start state is the grammar's start symbol, and the accept state is F.

FiniteAutomaton Class

The FiniteAutomaton class represents a finite automaton with attributes for states, alphabet, transitions, start state, and accept states.
Key Methods:

    string_belongs_to_language:

        This method checks if a given input string is accepted by the automaton.

        It simulates the automaton's operation by following the transitions for each symbol in the input string.

        If the final state after processing the string is an accept state, the string belongs to the language; otherwise, it does not.

Main Execution
    Iterating Through Productions:

        For each non-terminal (nt), the code examines all its possible productions.

        Each production represents a rule that defines how the non-terminal can be replaced.

    Handling Single-Symbol Productions:

        If the length of the production is 1 (e.g., A→aA→a), it signifies a transition to the final state F.

        This is because a single terminal symbol in the production means the non-terminal can be directly replaced by a terminal, leading to the end of the string.

        The transition is added to the transitions dictionary, mapping the non-terminal and the terminal symbol to the final state F.

    Handling Multi-Symbol Productions:

        If the production has more than one symbol (e.g., A→aBA→aB), it represents a transition to another non-terminal state.

        The first symbol of the production is a terminal (e.g., a), and the second symbol is a non-terminal (e.g., B).

        The transition is added to the transitions dictionary, mapping the non-terminal and the terminal symbol to the next state (e.g., B).

   ``` python
         for nt, productions in self.P.items():
            for production in productions:
                if len(production) == 1:  # A → a (transition to final)
                    transitions[nt][production[0]] = 'F'
                else:  # A → aB (transition to another state)
                    first_symbol = production[0]
                    next_state = production[1]
                    transitions[nt][first_symbol] = next_state
```

---
* ![image](https://github.com/user-attachments/assets/0ef2876b-6914-414e-9584-fc2026665b6b)



## Conclusions 
   This laboratory work provided a practical introduction to formal grammars and finite automata. By implementing a grammar and converting it into a finite automaton, we demonstrated the close relationship between these two concepts. The ability to generate valid strings and verify their acceptance by the automaton highlights the importance of these models in language processing and computational theory.

The project also emphasized the importance of structured implementation and clear documentation, which are essential for understanding and extending such systems. Future work could explore more complex grammars, such as context-free grammars, and their corresponding automata, as well as applications in parsing and compiler design.


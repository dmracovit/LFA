class Grammar:
    def __init__(self, non_terminals=None, terminals=None, productions=None, start_symbol=None):
        self.non_terminals = set(non_terminals) if non_terminals else set()
        self.terminals = set(terminals) if terminals else set()
        self.productions = productions or {}
        self.start_symbol = start_symbol
    
    def __str__(self):
        result = f"Non-terminals: {', '.join(sorted(self.non_terminals))}\n"
        result += f"Terminals: {', '.join(sorted(self.terminals))}\n"
        result += f"Start symbol: {self.start_symbol}\n"
        result += "Productions:\n"
        for nt in sorted(self.non_terminals):
            if nt in self.productions and self.productions[nt]:
                for prod in sorted(self.productions[nt]):
                    result += f"  {nt} -> {prod}\n"
        return result

    @classmethod
    def from_variant_26(cls):
        """Create a Grammar instance using the variant 26 data"""
        non_terminals = {'S', 'A', 'B', 'D'}
        terminals = {'a', 'b', 'd'}
        productions = {
            'S': ['aBA', 'AB'],
            'A': ['d', 'dS', 'AbBA', 'ε'],
            'B': ['a', 'aS'],
            'D': ['Aba']
        }
        return cls(non_terminals, terminals, productions, 'S')

    @classmethod
    def parse_grammar(cls, grammar_string):
        """Parse a grammar from a string representation"""
        lines = grammar_string.strip().split('\n')
        non_terminals = set()
        terminals = set()
        productions = {}
        start_symbol = None
        
        for line in lines:
            if '->' in line:
                left, right = line.split('->')
                left = left.strip()
                right = right.strip()
                
                if not start_symbol:
                    start_symbol = left
                
                non_terminals.add(left)
                
                if left not in productions:
                    productions[left] = []
                
                productions[left].append(right)
                
                for char in right:
                    if char.islower() or char in "ε":
                        terminals.add(char)
        
        # Remove epsilon from terminals if present
        if 'ε' in terminals:
            terminals.remove('ε')
            
        return cls(non_terminals, terminals, productions, start_symbol)

def convert_to_cnf(grammar):
    """Convert a grammar to Chomsky Normal Form"""
    print("\nStep 1: Create a new start symbol if needed")
    new_grammar = create_new_start_symbol(grammar)
    print(new_grammar)
    
    print("\nStep 2: Eliminate ε-productions")
    new_grammar = eliminate_epsilon_productions(new_grammar)
    print(new_grammar)
    
    print("\nStep 3: Eliminate unit productions")
    new_grammar = eliminate_unit_productions(new_grammar)
    print(new_grammar)
    
    print("\nStep 4: Replace terminal symbols in long productions")
    new_grammar = replace_terminals_in_long_productions(new_grammar)
    print(new_grammar)
    
    print("\nStep 5: Break productions with more than two symbols")
    new_grammar = break_long_productions(new_grammar)
    print(new_grammar)
    
    return new_grammar

def create_new_start_symbol(grammar):
    """Create a new start symbol S0 if the original appears on the right side"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    # Check if original start symbol appears on the right side of any production
    start_on_right = False
    for nt, prods in grammar.productions.items():
        for prod in prods:
            if grammar.start_symbol in prod:
                start_on_right = True
                break
        if start_on_right:
            break
    
    if start_on_right:
        new_start = 'S0'
        # Ensure the new symbol is unique
        while new_start in new_grammar.non_terminals:
            new_start += '0'
        
        new_grammar.non_terminals.add(new_start)
        new_grammar.productions[new_start] = [grammar.start_symbol]
        new_grammar.start_symbol = new_start
        print(f"Created new start symbol: {new_start}")
    else:
        print("No need for a new start symbol")
    
    return new_grammar

def eliminate_epsilon_productions(grammar):
    """Eliminate ε-productions from the grammar"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    # Find all nullable non-terminals (those that can derive ε)
    nullable = set()
    
    # First pass: Find directly nullable non-terminals
    for nt, prods in new_grammar.productions.items():
        if 'ε' in prods:
            nullable.add(nt)
            prods.remove('ε')
            print(f"Found directly nullable non-terminal: {nt}")
    
    # Find all indirectly nullable non-terminals until no new ones are found
    changed = True
    while changed:
        changed = False
        for nt, prods in new_grammar.productions.items():
            if nt not in nullable:
                for prod in prods:
                    if all(symbol in nullable for symbol in prod):
                        nullable.add(nt)
                        changed = True
                        print(f"Found indirectly nullable non-terminal: {nt}")
                        break
    
    print(f"All nullable non-terminals: {nullable}")
    
    # For each production, generate new ones by removing nullable symbols
    for nt, prods in list(new_grammar.productions.items()):
        new_prods = prods.copy()
        for prod in prods:
            # Find positions of nullable symbols
            nullable_positions = [i for i, symbol in enumerate(prod) if symbol in nullable]
            
            # Generate all possible combinations of removing nullable symbols
            # (except removing all of them which would create an ε-production)
            for mask in range(1, 2**len(nullable_positions)):
                positions_to_remove = [nullable_positions[i] 
                                      for i in range(len(nullable_positions)) 
                                      if (mask & (1 << i))]
                
                new_prod = ''.join(symbol for i, symbol in enumerate(prod) 
                                  if i not in positions_to_remove)
                
                # Don't add empty string unless it's for the start symbol and it's nullable
                if new_prod and new_prod not in new_prods:
                    new_prods.append(new_prod)
                    print(f"Added new production: {nt} -> {new_prod}")
        
        new_grammar.productions[nt] = new_prods
    
    # Special case: if the start symbol is nullable and should produce ε
    if new_grammar.start_symbol in nullable and all(len(prod) > 0 for prod in new_grammar.productions[new_grammar.start_symbol]):
        # Only add ε if the start symbol can't already derive it through other means
        can_derive_epsilon = False
        for prod in new_grammar.productions[new_grammar.start_symbol]:
            if all(symbol in nullable for symbol in prod):
                can_derive_epsilon = True
                break
        
        if not can_derive_epsilon:
            new_grammar.productions[new_grammar.start_symbol].append('ε')
            print(f"Added ε-production for start symbol: {new_grammar.start_symbol} -> ε")
    
    return new_grammar

def eliminate_unit_productions(grammar):
    """Eliminate unit productions (A -> B where B is a non-terminal)"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    # Find all unit pairs (A, B) where A can derive B
    unit_pairs = []
    for nt in new_grammar.non_terminals:
        find_unit_pairs(new_grammar, nt, nt, unit_pairs)
    
    print(f"Found unit pairs: {unit_pairs}")
    
    # Replace unit productions
    for a, b in unit_pairs:
        if a != b:  # Skip reflexive pairs
            if b in new_grammar.productions:
                for prod in new_grammar.productions[b]:
                    # Only add non-unit productions
                    if (len(prod) != 1 or prod not in new_grammar.non_terminals) and prod not in new_grammar.productions[a]:
                        new_grammar.productions[a].append(prod)
                        print(f"Added production from unit pair: {a} -> {prod}")
    
    # Remove unit productions
    for nt, prods in list(new_grammar.productions.items()):
        new_prods = [prod for prod in prods 
                    if len(prod) != 1 or prod not in new_grammar.non_terminals]
        removed = set(prods) - set(new_prods)
        if removed:
            print(f"Removed unit productions for {nt}: {', '.join(removed)}")
        new_grammar.productions[nt] = new_prods
    
    return new_grammar

def find_unit_pairs(grammar, start, current, unit_pairs):
    """Recursively find all unit pairs for a non-terminal"""
    pair = (start, current)
    if pair not in unit_pairs:
        unit_pairs.append(pair)
        if current in grammar.productions:
            for prod in grammar.productions[current]:
                if len(prod) == 1 and prod in grammar.non_terminals:
                    find_unit_pairs(grammar, start, prod, unit_pairs)

def replace_terminals_in_long_productions(grammar):
    """Replace terminal symbols in productions with more than one symbol"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    # Create non-terminals for each terminal
    terminal_to_nt = {}
    for terminal in grammar.terminals:
        terminal_nt = f"T_{terminal}"
        # Ensure the new symbol is unique
        while terminal_nt in new_grammar.non_terminals:
            terminal_nt += "_"
        
        terminal_to_nt[terminal] = terminal_nt
        new_grammar.non_terminals.add(terminal_nt)
        new_grammar.productions[terminal_nt] = [terminal]
        print(f"Created new non-terminal for terminal: {terminal_nt} -> {terminal}")
    
    # Replace terminals in productions with length > 1
    for nt, prods in list(new_grammar.productions.items()):
        new_prods = []
        for prod in prods:
            if len(prod) > 1:
                new_prod = ""
                for symbol in prod:
                    if symbol in grammar.terminals:
                        new_prod += terminal_to_nt[symbol]
                    else:
                        new_prod += symbol
                new_prods.append(new_prod)
                print(f"Replaced terminals in: {nt} -> {prod} becomes {nt} -> {new_prod}")
            else:
                new_prods.append(prod)
        new_grammar.productions[nt] = new_prods
    
    return new_grammar

def break_long_productions(grammar):
    """Break productions with more than two symbols"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    new_productions = {}
    for nt in new_grammar.non_terminals:
        new_productions[nt] = []
    
    next_new_nt = 0
    # Process each production
    for nt, prods in new_grammar.productions.items():
        for prod in prods:
            if len(prod) <= 2:
                # Productions of length 1 or 2 are already in the correct form
                new_productions[nt].append(prod)
            else:
                # Break down productions of length > 2
                print(f"Breaking down: {nt} -> {prod}")
                current_nt = nt
                symbols = list(prod)  # Convert to list for easier handling
                
                # Process all symbols except the last two
                for i in range(len(symbols) - 2):
                    new_nt = f"N{next_new_nt}"
                    next_new_nt += 1
                    
                    # Ensure the new non-terminal is unique
                    while new_nt in new_grammar.non_terminals:
                        new_nt = f"N{next_new_nt}"
                        next_new_nt += 1
                    
                    new_grammar.non_terminals.add(new_nt)
                    if new_nt not in new_productions:
                        new_productions[new_nt] = []
                    
                    # Add a new production: current_nt -> first_symbol new_nt
                    new_productions[current_nt].append(symbols[i] + new_nt)
                    print(f"  Added: {current_nt} -> {symbols[i] + new_nt}")
                    
                    # Update current_nt for the next iteration
                    current_nt = new_nt
                
                # Add the last production with the last two symbols
                last_prod = symbols[-2] + symbols[-1]
                new_productions[current_nt].append(last_prod)
                print(f"  Added: {current_nt} -> {last_prod}")
    
    new_grammar.productions = new_productions
    return new_grammar

def main():
    print("Chomsky Normal Form Converter")
    print("----------------------------\n")
    
    # Get grammar from variant 26
    grammar = Grammar.from_variant_26()
    print("Original Grammar:")
    print(grammar)
    
    # Convert to CNF
    cnf_grammar = convert_to_cnf(grammar)
    print("\nFinal Grammar in Chomsky Normal Form:")
    print(cnf_grammar)
    
    # BONUS: Allowing any input grammar
    print("\nBonus: Convert a custom grammar to CNF")
    print("Enter your grammar in the format 'A -> aBc' (one production per line).")
    print("Enter a blank line to finish input.")
    
    custom_grammar_str = ""
    while True:
        line = input()
        if not line:
            break
        custom_grammar_str += line + "\n"
    
    if custom_grammar_str:
        try:
            custom_grammar = Grammar.parse_grammar(custom_grammar_str)
            print("\nCustom Grammar:")
            print(custom_grammar)
            
            cnf_custom_grammar = convert_to_cnf(custom_grammar)
            print("\nCustom Grammar in Chomsky Normal Form:")
            print(cnf_custom_grammar)
        except Exception as e:
            print(f"Error processing custom grammar: {e}")

if __name__ == "__main__":
    main()
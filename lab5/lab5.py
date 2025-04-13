class Grammar:
    def __init__(self, variables, terminals, productions, start_symbol):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
    
    def __str__(self):
        prod_str = "\n".join([f"{k} → {' | '.join(v)}" for k, v in self.productions.items()])
        return f"Variables: {self.variables}\nTerminals: {self.terminals}\nStart: {self.start_symbol}\nProductions:\n{prod_str}"

def eliminate_epsilon_productions(grammar):
    # Step 1: Find all nullable variables
    nullable = set()
    changed = True
    while changed:
        changed = False
        for var in grammar.variables:
            for prod in grammar.productions.get(var, []):
                if prod == 'ε' or all(symbol in nullable for symbol in prod):
                    if var not in nullable:
                        nullable.add(var)
                        changed = True
    
    # Step 2: Remove ε-productions and add new productions
    new_productions = {}
    for var in grammar.variables:
        new_productions[var] = []
        for prod in grammar.productions.get(var, []):
            if prod != 'ε':
                # Generate all possible combinations without nullable symbols
                from itertools import product
                positions = [i for i, symbol in enumerate(prod) if symbol in nullable]
                for mask in product([False, True], repeat=len(positions)):
                    new_prod = list(prod)
                    for i, pos in enumerate(positions):
                        if mask[i]:
                            new_prod[pos] = ''
                    new_prod = ''.join([c for c in new_prod if c != ''])
                    if new_prod != '' and new_prod not in new_productions[var]:
                        new_productions[var].append(new_prod)
    
    grammar.productions = new_productions
    return grammar

def eliminate_unit_productions(grammar):
    changed = True
    while changed:
        changed = False
        unit_pairs = []
        # Find all unit productions (A → B)
        for var in grammar.variables:
            for prod in grammar.productions.get(var, []):
                if len(prod) == 1 and prod in grammar.variables:
                    unit_pairs.append((var, prod))
        
        # Replace unit productions
        for A, B in unit_pairs:
            for prod in grammar.productions.get(B, []):
                if len(prod) != 1 or prod not in grammar.variables:
                    if prod not in grammar.productions[A]:
                        grammar.productions[A].append(prod)
                        changed = True
            if (A, B) in [(v, p) for v in grammar.variables for p in grammar.productions.get(v, [])]:
                grammar.productions[A].remove(B)
                changed = True
    return grammar

def eliminate_inaccessible_symbols(grammar):
    accessible = {grammar.start_symbol}
    changed = True
    while changed:
        changed = False
        for var in list(accessible):
            for prod in grammar.productions.get(var, []):
                for symbol in prod:
                    if symbol in grammar.variables and symbol not in accessible:
                        accessible.add(symbol)
                        changed = True
    
    # Remove inaccessible symbols
    new_variables = [v for v in grammar.variables if v in accessible]
    new_productions = {k: v for k, v in grammar.productions.items() if k in accessible}
    
    grammar.variables = new_variables
    grammar.productions = new_productions
    return grammar

def eliminate_non_productive(grammar):
    productive = set()
    # Start with variables that have terminal productions
    for var in grammar.variables:
        for prod in grammar.productions.get(var, []):
            if all(symbol in grammar.terminals for symbol in prod):
                productive.add(var)
    
    changed = True
    while changed:
        changed = False
        for var in grammar.variables:
            if var not in productive:
                for prod in grammar.productions.get(var, []):
                    if all(symbol in productive or symbol in grammar.terminals for symbol in prod):
                        productive.add(var)
                        changed = True
    
    # Remove non-productive symbols
    new_variables = [v for v in grammar.variables if v in productive]
    new_productions = {k: [p for p in v if all(s in productive or s in grammar.terminals for s in p)] 
                      for k, v in grammar.productions.items() if k in productive}
    
    grammar.variables = new_variables
    grammar.productions = new_productions
    return grammar

def to_chomsky_normal_form(grammar):
    # Step 1: Eliminate ε-productions
    grammar = eliminate_epsilon_productions(grammar)
    
    # Step 2: Eliminate unit productions
    grammar = eliminate_unit_productions(grammar)
    
    # Step 3: Eliminate inaccessible symbols
    grammar = eliminate_inaccessible_symbols(grammar)
    
    # Step 4: Eliminate non-productive symbols
    grammar = eliminate_non_productive(grammar)
    
    # Step 5: Convert to CNF
    # Create new productions for terminals
    terminal_to_var = {}
    new_vars = []
    for terminal in grammar.terminals:
        new_var = f"T_{terminal}"
        terminal_to_var[terminal] = new_var
        new_vars.append(new_var)
    
    grammar.variables.extend(new_vars)
    for terminal, var in terminal_to_var.items():
        grammar.productions[var] = [terminal]
    
    # Replace terminals in productions with their new variables
    new_productions = {}
    for var in grammar.variables:
        new_productions[var] = []
        for prod in grammar.productions.get(var, []):
            if len(prod) > 1:
                new_prod = []
                for symbol in prod:
                    if symbol in grammar.terminals:
                        new_prod.append(terminal_to_var[symbol])
                    else:
                        new_prod.append(symbol)
                new_prod = ''.join(new_prod)
                new_productions[var].append(new_prod)
            else:
                new_productions[var].append(prod)
    
    grammar.productions = new_productions
    
    # Break down productions with more than 2 symbols
    next_var_num = 0
    changed = True
    while changed:
        changed = False
        new_productions = {}
        for var in grammar.variables:
            new_productions[var] = []
            for prod in grammar.productions.get(var, []):
                if len(prod) > 2:
                    changed = True
                    # Split into two parts
                    first_part = prod[0]
                    remaining = prod[1:]
                    new_var = f"N_{next_var_num}"
                    next_var_num += 1
                    grammar.variables.append(new_var)
                    new_productions[var].append(first_part + new_var)
                    new_productions[new_var] = [remaining]
                else:
                    new_productions[var].append(prod)
        grammar.productions = new_productions
    
    return grammar

# Your variant grammar
variables = ['S', 'A', 'B', 'D']
terminals = ['a', 'b', 'd']
productions = {
    'S': ['aBA', 'AB'],
    'A': ['d', 'dS', 'AbBA', 'ε'],
    'B': ['a', 'aS', 'A'],
    'D': ['Aba']
}
start_symbol = 'S'

grammar = Grammar(variables, terminals, productions, start_symbol)

# Convert to CNF
cnf_grammar = to_chomsky_normal_form(grammar)

# Print the CNF grammar
print("Variables:", cnf_grammar.variables)
print("Terminals:", cnf_grammar.terminals)
print("Start Symbol:", cnf_grammar.start_symbol)
print("Productions:")
for var in cnf_grammar.variables:
    if var in cnf_grammar.productions:
        print(f"{var} → {' | '.join(cnf_grammar.productions[var])}")
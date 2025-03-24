# Lexical Analyzer for a Music Scripting Language

### Course: Formal Languages & Finite Automata  
### Author: Racovita Dumitru

---

## Theory  
A lexical analyzer, or lexer, is a fundamental component of a compiler or interpreter. It processes the input text (source code) and breaks it down into meaningful tokens, which are the smallest units of syntax (e.g., keywords, identifiers, operators). These tokens are then passed to the parser for further processing.  

In this project, a lexer is implemented for a custom music scripting language. The language includes constructs for defining musical chunks, time signatures, tempo, volume, instruments (e.g., piano, guitar), and control structures like loops and synchronization.  

---

## Objectives:  
1. To design and implement a lexical analyzer for a custom music scripting language.  
2. To tokenize input text into meaningful components such as keywords, identifiers, and symbols.  
3. To ignore irrelevant characters like whitespace and newlines.  
4. To provide a clear and structured output of tokens for further processing.  

---

## Implementation Description  

### Token Definitions  
The lexer uses a list of token types (`TOKEN_TYPES`), where each token type is defined by a name and a regular expression pattern. For example:  
- `CHUNK`: Matches patterns like `chunk1`, `chunk2`, etc.  
- `TIME_SIGNATURE`: Matches patterns like `TimeSignature=4/4`.  
- `PIANO`: Matches the keyword `Piano`.  
- `IDENTIFIER`: Matches variable names or labels like `note`, `do`, `sol`.  
- `FRACTION`: Matches musical note durations like `2/4`, `1/4`.  
- `WHITESPACE`: Matches spaces, tabs, and newlines (ignored during tokenization).  

The `TOKEN_REGEX` combines all these patterns into a single regular expression using the `|` (OR) operator. Each pattern is named using the `?P<name>` syntax for easy identification.  

### Loop

  We can have 2 main use cases for loops. Loops for changing the notes at each interation, another for just repeating the same music certain amount of times
  
    for(note = re; note < si; note+=1){
    piano(R, note, 1/4)
    }
    for(i = 0; i < 10; note+=1){
    piano(R, re, 1/4)
    } 

### Piano
Piano has too many keys to be expressed only in 5 rows on musical sheet. This is why pianists use 2 rows to define the notes. One for the right hand (starts with Sol cleff), another for the left hand (bas key)
![image](https://github.com/user-attachments/assets/ad23c75d-69cd-4058-aca5-cc124f6aaa4b)

### Guitar
As you maybe know the guitar has 6 strings with it's notation for each string expressed in letters of the English alphabet (A-F). Also for each sound on the guitar cliff there are their own notations, so we are lucky. To read from the lowest sound to the highest go from bottom row to the right, go to the beginning of the row above and repeat:
![image](https://github.com/user-attachments/assets/fe6e0d57-2126-4560-bec1-18826530bd81)


 
### Lexer Class  
The `Lexer` class is responsible for tokenizing the input text. It has two main methods:  
1. `tokenize()`: Uses `re.finditer` to match tokens in the input text based on `TOKEN_REGEX`. It skips whitespace and appends valid tokens to the `tokens` list.  
2. `next_token()`: Returns the next token from the list and removes it (simulating a token stream).  

### Example Input and Output  
Here is an example input:  

```python
code = """
chunk1 {
    TimeSignature=4/4
    Tempo=120
    Volume=80
    Piano(R, do, 2/4)
    Piano(L, sol, 1/4)
    sync {
        Piano(R, re, 1/4)
        Piano(R, mi, 1/4)
    }
    for(note = do; note < sol; note+=1){
        Piano(R, note, 1/4)
    }
}
```

  
```python

'''
('CHUNK', 'chunk1')
('LBRACE', '{')
('TIME_SIGNATURE', 'TimeSignature=4/4')
('TEMPO', 'Tempo=120')
('VOLUME', 'Volume=80')
('PIANO', 'Piano')
('LPAREN', '(')
('IDENTIFIER', 'R')
('COMMA', ',')
('IDENTIFIER', 'do')
('COMMA', ',')
('FRACTION', '2/4')
('RPAREN', ')')
('PIANO', 'Piano')
('LPAREN', '(')
('IDENTIFIER', 'L')
('COMMA', ',')
('IDENTIFIER', 'sol')
('COMMA', ',')
('FRACTION', '1/4')
('RPAREN', ')')
('SYNC', 'sync')
('LBRACE', '{')
('PIANO', 'Piano')
('LPAREN', '(')
('IDENTIFIER', 'R')
('COMMA', ',')
('IDENTIFIER', 're')
('COMMA', ',')
('FRACTION', '1/4')
('RPAREN', ')')
('PIANO', 'Piano')
('LPAREN', '(')
('IDENTIFIER', 'R')
('COMMA', ',')
('IDENTIFIER', 'mi')
('COMMA', ',')
('FRACTION', '1/4')
('RPAREN', ')')
('RBRACE', '}')
('LOOP', 'for')
('LPAREN', '(')
('IDENTIFIER', 'note')
('EQUALS', '=')
('IDENTIFIER', 'do')
('SEMICOLON', ';')
('IDENTIFIER', 'note')
('LESS', '<')
('IDENTIFIER', 'sol')
('SEMICOLON', ';')
('IDENTIFIER', 'note')
('PLUS_EQUALS', '+=')
('NUMBER', '1')
('RPAREN', ')')
('LBRACE', '{')
('PIANO', 'Piano')
('LPAREN', '(')
('IDENTIFIER', 'R')
('COMMA', ',')
('IDENTIFIER', 'note')
('COMMA', ',')
('FRACTION', '1/4')
('RPAREN', ')')
('RBRACE', '}')
('RBRACE', '}')
('EOF', None)
```

## Conclusion
The lexer successfully tokenizes the input text into meaningful components, ignoring irrelevant characters like whitespace. 
It provides a structured output that can be used by a parser to build an abstract syntax tree (AST) or execute the script directly.
This implementation demonstrates the foundational role of lexical analysis in language processing.



# Laboratory Work #4: Regular Expression Generator

**Course:** Formal Languages & Finite Automata  
**Author:** Racovita Dumitru FAF-233 

---

## Theory  
Regular expressions are powerful tools for pattern matching in strings. They consist of:
- **Literals** (exact characters like `a`, `2`)
- **Metacharacters** (special symbols like `*`, `+`, `|`)
- **Quantifiers** (specify repetitions like `{n}`, `^+`)

In this lab, we implement a dynamic regex interpreter that generates valid strings from given patterns while tracking the processing steps.

---

## Objectives
1. Understand regular expression syntax and components
2. Implement a dynamic regex string generator
3. Visualize the step-by-step processing (bonus)

---

## Implementation Description

### 1. Core Class Structure
The `RegexGenerator` class handles all processing:

```python
class RegexGenerator:
    def __init__(self, max_repeat=5):
        self.max_repeat = max_repeat  # Limits repetitions
        self.processing_steps = OrderedDict()  # Tracks transformations
```

2. Processing Pipeline

Four key steps transform regex to strings:
Step 1: Exponent Handling

Converts ^ notation to standard quantifiers:
python
```
pattern = re.sub(r'(\w)\^\+', lambda m: f"{m.group(1)}{{1,{self.max_repeat}}}", pattern)
```
Step 2: Alternation Resolution

Randomly selects alternatives:
python
```

pattern = re.sub(r'\(([^)]+)\)', lambda m: random.choice(m.group(1).split('|')), pattern)
```
Step 3: Quantifier Expansion

Processes *, +, ?, {n}:
python
```

pattern = re.sub(r'(\w)\*', lambda m: m.group(1)*random.randint(0, self.max_repeat), pattern)
```
Step 4: Cleanup

Removes residual syntax markers:
python
```

pattern = pattern.replace('·', '')
```
3. Bonus: Processing Visualization
python
```

def print_steps(self):
    for step, data in self.processing_steps.items():
        print(f"Step {step}: {data['explanation']}")
        print(f"  Before: {data['before']}")
        print(f"  After: {data['after']}")
```
Results
Example 1: Pattern (a|b)(c|d)E^+G?
Copy

Processing Steps:
1. Converted ^+ to {1,5} → (a|b)(c|d)E{1,5}G?
2. Resolved alternations → bdE{1,5}G?
3. Applied quantifiers → bdEEEG
Final Result: bdEEEG

Example 2: Pattern 1(0|1)*2(3|4)^536
Copy

Processing Steps:
1. Converted ^5 to {5} → 1(0|1)*2(3|4){5}36
2. Resolved alternations → 1102(3|4){5}36
3. Applied quantifiers → 11023333336
Final Result: 11023333336

Conclusion

This implementation:

    Successfully generates valid strings from complex regex patterns

    Provides clear visualization of processing steps

    Handles all specified regex operators dynamically

The main challenge was properly ordering the processing steps to avoid conflicts between different regex operators. The solution demonstrates how regular expressions can be systematically interpreted and executed.

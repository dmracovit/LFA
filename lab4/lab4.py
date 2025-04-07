import random
import re
from collections import OrderedDict

class RegexGenerator:
    def __init__(self, max_repeat=5):
        self.max_repeat = max_repeat
        self.processing_steps = OrderedDict()
    
    def _log_step(self, stage, before, after, explanation):
        """Records each processing step with visual diff"""
        self.processing_steps[stage] = {
            'before': before,
            'after': after,
            'explanation': explanation
        }
    
    def generate(self, pattern):
        self.processing_steps.clear()
        original = pattern
        self._log_step("0_Start", pattern, None, "Original pattern")
        
        # Processing pipeline
        pattern = self._process_exponents(pattern)
        pattern = self._process_alternations(pattern)
        pattern = self._process_quantifiers(pattern)
        pattern = self._clean_special_chars(pattern)
        
        return {
            'original': original,
            'result': pattern,
            'steps': self.processing_steps
        }
    
    def _process_exponents(self, pattern):
        """Step 1: Handle ^+ and ^n notation"""
        new_pattern = re.sub(
            r'(\w)\^\+', 
            lambda m: f"{m.group(1)}{{1,{self.max_repeat}}}", 
            pattern
        )
        new_pattern = re.sub(
            r'(\w)\^(\d+)', 
            lambda m: f"{m.group(1)}{{{m.group(2)}}}", 
            new_pattern
        )
        self._log_step("1_Exponents", pattern, new_pattern, 
                      "Converted ^+ to {1,N} and ^n to {n}")
        return new_pattern
    
    def _process_alternations(self, pattern):
        """Step 2: Handle (a|b) choices"""
        new_pattern = pattern
        while '|' in new_pattern:
            prev = new_pattern
            new_pattern = re.sub(
                r'\(([^)]+)\)', 
                lambda m: random.choice(m.group(1).split('|')), 
                new_pattern
            )
            if new_pattern != prev:
                self._log_step("2_Alternations", prev, new_pattern, 
                             f"Resolved alternation: {prev} → {new_pattern}")
        return new_pattern
    
    def _process_quantifiers(self, pattern):
        """Step 3: Handle all quantifiers"""
        new_pattern = pattern
        
        # Process {n,m} ranges
        new_pattern = re.sub(
            r'\{(\d+),(\d+)\}', 
            lambda m: m.group(1) * random.randint(int(m.group(1)), int(m.group(2))), 
            new_pattern
        )
        
        # Process fixed {n}
        new_pattern = re.sub(
            r'\{(\d+)\}', 
            lambda m: m.group(1) * int(m.group(2)), 
            new_pattern
        )
        
        # Process *, +, ?
        quant_map = [
            (r'(\w)\*', lambda m: m.group(1) * random.randint(0, self.max_repeat)),
            (r'(\w)\+', lambda m: m.group(1) * random.randint(1, self.max_repeat)),
            (r'(\w)\?', lambda m: m.group(1) if random.random() > 0.5 else '')
        ]
        
        for q_pattern, q_func in quant_map:
            prev = new_pattern
            new_pattern = re.sub(q_pattern, q_func, new_pattern)
            if new_pattern != prev:
                self._log_step("3_Quantifiers", prev, new_pattern, 
                             f"Applied {q_pattern} quantifier")
        
        return new_pattern
    
    def _clean_special_chars(self, pattern):
        """Step 4: Final cleanup"""
        new_pattern = pattern.replace('·', '').replace('^', '')
        if new_pattern != pattern:
            self._log_step("4_Cleanup", pattern, new_pattern, 
                          "Removed special characters")
        return new_pattern
    
    def print_processing_steps(self, result):
        """Beautiful step-by-step visualization"""
        print(f"\n{' REGEX PROCESSING STEPS ':=^60}")
        print(f"Original: {result['original']}\n")
        
        for stage, data in result['steps'].items():
            step_num = stage.split('_')[0]
            print(f"{step_num}. {data['explanation']}")
            if data['after'] is not None:
                print(f"   Before: {data['before']}")
                print(f"   After:  {data['after']}")
            print()
        
        print(f"Final Result: {result['result']}")
        print('='*60 + "\n")

def generate_variant1_with_bonus():
    generator = RegexGenerator()
    
    # Pattern 1: (a|b)(c|d)E^+G?
    print("\n" + "="*20 + " PATTERN 1 " + "="*20)
    p1 = "(a|b)(c|d)E^+G?"
    result1 = generator.generate(p1)
    print(f"Generated: {result1['result']}")
    generator.print_processing_steps(result1)
    
    # Pattern 2: P(Q|R|S)T(uv|w|x)*Z+
    print("\n" + "="*20 + " PATTERN 2 " + "="*20)
    p2 = "P(Q|R|S)T(uv|w|x)*Z+"
    result2 = generator.generate(p2)
    print(f"Generated: {result2['result']}")
    generator.print_processing_steps(result2)
    
    # Pattern 3: 1(0|1)*2(3|4)^536
    print("\n" + "="*20 + " PATTERN 3 " + "="*20)
    p3 = "1(0|1)*2(3|4)^536"
    result3 = generator.generate(p3)
    print(f"Generated: {result3['result']}")
    generator.print_processing_steps(result3)

generate_variant1_with_bonus()
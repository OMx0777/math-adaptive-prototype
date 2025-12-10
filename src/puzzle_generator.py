"""
Puzzle Generates math problems based on difficulty level
"""
import random

class PuzzleGenerator:
    def __init__(self):
        self.difficulty_levels = {
            'easy': {'range': (1, 10), 'operations': ['+', '-']},
            'medium': {'range': (10, 50), 'operations': ['+', '-', '*']},
            'hard': {'range': (20, 100), 'operations': ['+', '-', '*', '/']}
        }
    
    def generate_puzzle(self, difficulty='easy'):
        """
        Generate a math puzzle based on difficulty level
        
        Args:
            difficulty (str): 'easy', 'medium', or 'hard'
        
        Returns:
            dict: Contains question, answer, and metadata
        """
        config = self.difficulty_levels.get(difficulty.lower(), self.difficulty_levels['easy'])
        num_range = config['range']
        operations = config['operations']
        
        # Select random operation
        operation = random.choice(operations)
        
        # Generate numbers based on operation
        if operation == '/':
            # Ensure clean division for division problems
            divisor = random.randint(2, max(3, num_range[1] // 5))
            max_quotient = num_range[1] // divisor
            min_quotient = max(1, num_range[0] // divisor)
            
            # Ensure valid range for quotient
            if min_quotient > max_quotient:
                min_quotient = 2
                max_quotient = max(3, num_range[1] // divisor)
            
            quotient = random.randint(min_quotient, max_quotient)
            num1 = divisor * quotient
            num2 = divisor
            answer = quotient
        else:
            num1 = random.randint(num_range[0], num_range[1])
            num2 = random.randint(num_range[0], num_range[1])
            
            # Calculate answer based on operation
            if operation == '+':
                answer = num1 + num2
            elif operation == '-':
                # Ensure non-negative results for subtraction
                if num1 < num2:
                    num1, num2 = num2, num1
                answer = num1 - num2
            elif operation == '*':
                answer = num1 * num2
        
        question = f"{num1} {operation} {num2}"
        
        return {
            'question': question,
            'answer': answer,
            'difficulty': difficulty,
            'operation': operation
        }
    
    def get_difficulty_levels(self):
        """Return available difficulty levels"""
        return list(self.difficulty_levels.keys())
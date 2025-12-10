"""
This is my main app with terminal interface
"""
import time
import sys
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

class MathAdventure:
    def __init__(self):
        self.generator = PuzzleGenerator()
        self.tracker = None
        self.engine = None
        self.current_difficulty = 'easy'
        
    def display_welcome(self):
        #Display welcome message
        print("\n" + "="*60)
        print("MATH ADVENTURES - AI-Powered Adaptive Learning")
        print("="*60)
        print("\nWelcome This system adapts to your performance automatically.")
        print("The more you practice, the better it understands your level\n")
    
    def get_user_info(self):
        #Get user information and initial settings
        name = input("Enter your name: ").strip()
        if not name:
            name = "Student"
        
        print(f"\nHello, {name}")
        print("\nChoose your starting difficulty:")
        print("1. Easy (numbers 1-10, +/-)")
        print("2. Medium (numbers 10-50, +/-/*)")
        print("3. Hard (numbers 20-100, +/-/*/÷)")
        
        choice = input("\nEnter choice (1/2/3) [default: 1]: ").strip()
        difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
        self.current_difficulty = difficulty_map.get(choice, 'easy')
        
        print("\nChoose adaptation method:")
        print("1. Rule-based (uses accuracy, time, and streak)")
        print("2. ML-based (uses weighted performance scoring)")
        
        method_choice = input("\nEnter choice (1/2) [default: 1]: ").strip()
        method = 'ml-based' if method_choice == '2' else 'rule-based'
        
        self.tracker = PerformanceTracker(name)
        self.engine = AdaptiveEngine(method=method, window_size=5)
        
        print(f"\n Starting at {self.current_difficulty.upper()} level")
        print(f" Using {method.upper()} adaptation")
        print("\nType 'quit' or 'exit' anytime to end the session.\n")
        time.sleep(1)
    
    def play_round(self, round_num):
        #Play a single puzzle round
        print(f"\n{'─'*60}")
        print(f"Round {round_num} | Current Level: {self.current_difficulty.upper()}")
        print('─'*60)
        
        # Generate puzzle
        puzzle = self.generator.generate_puzzle(self.current_difficulty)
        print(f"\nSolve: {puzzle['question']} = ?")
        
        # Get user answer with timing
        start_time = time.time()
        user_input = input("\nYour answer: ").strip().lower()
        end_time = time.time()
        
        # Check for quit
        if user_input in ['quit', 'exit', 'q']:
            return False
        
        # Validate and check answer
        try:
            user_answer = float(user_input)
            time_taken = end_time - start_time
            is_correct = abs(user_answer - puzzle['answer']) < 0.01
            
            # Log the attempt
            self.tracker.log_attempt(puzzle, user_answer, time_taken, is_correct)
            
            # Provide feedback
            if is_correct:
                print(f"✓ Correct! ({time_taken:.1f}s)")
                if self.tracker.current_streak >= 3:
                    print(f"yooooooo!!!!!!!! {self.tracker.current_streak} in a row!")
            else:
                print(f" nooooooo!!!!!! The answer was {puzzle['answer']}")
                if self.tracker.current_streak > 0:
                    print(f"   (Streak broken at {self.tracker.current_streak})")
            
            # Get adaptive recommendation after enough attempts
            if len(self.tracker.attempts) >= 3:
                new_difficulty, reasoning = self.engine.recommend_difficulty(
                    self.tracker, 
                    self.current_difficulty
                )
                
                if new_difficulty != self.current_difficulty:
                    print(f"\nDifficulty adjusted: {self.current_difficulty.upper()} → {new_difficulty.upper()}")
                    print(f"   Reason: {reasoning}")
                    self.current_difficulty = new_difficulty
                else:
                    if round_num % 5 == 0:  # Show reasoning every 5 rounds
                        print(f"\n:-> {reasoning}")
            
            return True
            
        except ValueError:
            print("Please enter a valid number")
            return True
    
    def display_summary(self):
        #Display session summary
        summary = self.tracker.get_session_summary()
        
        print("\n" + "="*60)
        print("SESSION SUMMARY")
        print("="*60)
        
        print(f"\nStudent: {summary['user_name']}")
        print(f"  Session Duration: {summary['session_duration']:.0f} seconds")
        print(f"\n Overall Performance:")
        print(f"   Total Puzzles: {summary['total_attempts']}")
        print(f"   Correct Answers: {summary['correct_answers']}")
        print(f"   Accuracy: {summary['overall_accuracy']:.1f}%")
        print(f"   Avg Time/Puzzle: {summary['avg_time_per_puzzle']:.1f}s")
        print(f"   Best Streak: {summary['max_streak']}")
        
        print(f"\nPerformance by Difficulty:")
        for diff, stats in summary['difficulty_stats'].items():
            print(f"   {diff.capitalize()}: {stats['accuracy']*100:.1f}% accuracy "
                  f"({stats['attempts']} attempts, {stats['avg_time']:.1f}s avg)")
        
        print(f"\n Performance by Operation:")
        for op, stats in summary['operation_stats'].items():
            print(f"   {op}: {stats['accuracy']*100:.1f}% accuracy ({stats['attempts']} attempts)")
        
        # Next session recommendation
        next_level = self.engine.get_next_recommended_level(self.tracker)
        print(f"\n Recommended starting level for next session: {next_level.upper()}")
        
        # Personalized feedback
        print(f"\n Feedback:")
        if summary['overall_accuracy'] >= 80:
            print("  WOWWW Excellent work You're mastering these concepts.")
        elif summary['overall_accuracy'] >= 60:
            print("  WOWW Good progress! Keep practicing to improve accuracy.")
        else:
            print("  Keep practicing Everyone learns at their own pace.")
        
        print("\n" + "="*60)
    
    def run(self):
        #Main application loop
        try:
            self.display_welcome()
            self.get_user_info()
            
            round_num = 1
            while True:
                continue_playing = self.play_round(round_num)
                if not continue_playing:
                    break
                
                round_num += 1
                
                # Optional: Ask to continue every 10 rounds
                if round_num % 10 == 1 and round_num > 1:
                    cont = input("\n Continue playing? (y/n): ").strip().lower()
                    if cont in ['n', 'no']:
                        break
            
            # Display final summary
            self.display_summary()
            print("\nThank you for learning with Math Adventures! \n")
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted by user.")
            if self.tracker and self.tracker.attempts:
                self.display_summary()
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            sys.exit(1)

def main():
    app = MathAdventure()
    app.run()

if __name__ == "__main__":
    main()

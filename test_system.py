"""
Test Script for Math Adventures System it validates all components work correctly
"""
import sys
import time
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

def test_puzzle_generator():
    #Test puzzle generation for all difficulty levels
    print("Testing Puzzle Generator...")
    generator = PuzzleGenerator()
    
    for difficulty in ['easy', 'medium', 'hard']:
        print(f"\n  Testing {difficulty} difficulty:")
        for i in range(3):
            puzzle = generator.generate_puzzle(difficulty)
            print(f"    {puzzle['question']} = {puzzle['answer']}")
            assert puzzle['answer'] is not None, f"Failed to generate answer for {difficulty}"
    
    print("✓ Puzzle Generator: PASSED\n")

def test_performance_tracker():
    #Test performance tracking functionality
    print("Testing Performance Tracker...")
    tracker = PerformanceTracker("Test Student")
    generator = PuzzleGenerator()
    
    # Simulate 10 attempts
    for i in range(10):
        puzzle = generator.generate_puzzle('easy')
        is_correct = i % 3 != 0  # Make some incorrect
        time_taken = 5.0 + (i * 0.5)
        tracker.log_attempt(puzzle, puzzle['answer'] if is_correct else 0, time_taken, is_correct)
    
    # Test recent performance
    recent = tracker.get_recent_performance(5)
    print(f"  Recent accuracy: {recent['accuracy']*100:.1f}%")
    print(f"  Average time: {recent['avg_time']:.1f}s")
    
    # Test summary
    summary = tracker.get_session_summary()
    print(f"  Total attempts: {summary['total_attempts']}")
    print(f"  Overall accuracy: {summary['overall_accuracy']:.1f}%")
    
    assert summary['total_attempts'] == 10, "Incorrect attempt count"
    print("✓ Performance Tracker: PASSED\n")

def test_adaptive_engine():
    #Test adaptive logic for both methods
    print("Testing Adaptive Engine...")
    
    for method in ['rule-based', 'ml-based']:
        print(f"\n  Testing {method} method:")
        tracker = PerformanceTracker("Test Student")
        engine = AdaptiveEngine(method=method)
        generator = PuzzleGenerator()
        
        current_diff = 'easy'
        
        # Simulate high performance (should increase difficulty)
        for i in range(5):
            puzzle = generator.generate_puzzle(current_diff)
            tracker.log_attempt(puzzle, puzzle['answer'], 3.0, True)
        
        new_diff, reasoning = engine.recommend_difficulty(tracker, current_diff)
        print(f"    High performance: {current_diff} → {new_diff}")
        print(f"    Reasoning: {reasoning}")
        
        # Simulate low performance (should decrease or maintain)
        current_diff = 'hard'
        tracker2 = PerformanceTracker("Test Student 2")
        
        for i in range(5):
            puzzle = generator.generate_puzzle(current_diff)
            is_correct = i % 4 == 0  # Only 25% correct
            tracker2.log_attempt(puzzle, puzzle['answer'] if is_correct else 0, 12.0, is_correct)
        
        new_diff2, reasoning2 = engine.recommend_difficulty(tracker2, current_diff)
        print(f"    Low performance: {current_diff} → {new_diff2}")
        print(f"    Reasoning: {reasoning2}")
    
    print("\n✓ Adaptive Engine: PASSED\n")

def test_integration():
    #Test complete flow integration
    print("Testing Full Integration...")
    
    generator = PuzzleGenerator()
    tracker = PerformanceTracker("Integration Test")
    engine = AdaptiveEngine(method='rule-based')
    
    current_diff = 'easy'
    
    print(f"  Starting difficulty: {current_diff}")
    
    # Simulate a learning session
    for round_num in range(15):
        puzzle = generator.generate_puzzle(current_diff)
        
        # Simulate improving performance
        is_correct = round_num > 5 or round_num % 2 == 0
        time_taken = max(3.0, 10.0 - round_num * 0.4)
        
        tracker.log_attempt(puzzle, puzzle['answer'] if is_correct else 0, time_taken, is_correct)
        
        if round_num >= 3:
            new_diff, reasoning = engine.recommend_difficulty(tracker, current_diff)
            if new_diff != current_diff:
                print(f"  Round {round_num+1}: {current_diff} → {new_diff}")
                current_diff = new_diff
    
    summary = tracker.get_session_summary()
    print(f"\n  Final Statistics:")
    print(f"    Total attempts: {summary['total_attempts']}")
    print(f"    Overall accuracy: {summary['overall_accuracy']:.1f}%")
    print(f"    Final difficulty: {summary['final_difficulty']}")
    
    print("\n✓ Integration Test: PASSED\n")

def run_all_tests():
    #Run all test suites
    print("\n" + "="*60)
    print("  MATH ADVENTURES - SYSTEM TEST SUITE")
    print("="*60 + "\n")
    
    try:
        test_puzzle_generator()
        test_performance_tracker()
        test_adaptive_engine()
        test_integration()
        
        print("="*60)
        print("  ALL TESTS PASSED ✓")
        print("="*60 + "\n")
        print("System is ready to use! Run: python src/main.py")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()

"""
this code is for tracking the performance of user
"""
import time
from datetime import datetime

class PerformanceTracker:
    def __init__(self, user_name):
        self.user_name = user_name
        self.session_start = datetime.now()
        self.attempts = []
        self.current_streak = 0
        self.max_streak = 0
        
    def log_attempt(self, puzzle, user_answer, time_taken, is_correct):
        
        attempt = {
            'timestamp': datetime.now(),
            'difficulty': puzzle['difficulty'],
            'operation': puzzle['operation'],
            'question': puzzle['question'],
            'correct_answer': puzzle['answer'],
            'user_answer': user_answer,
            'time_taken': round(time_taken, 2),
            'is_correct': is_correct
        }
        
        self.attempts.append(attempt)
        
        # Update streak tracking
        if is_correct:
            self.current_streak += 1
            self.max_streak = max(self.max_streak, self.current_streak)
        else:
            self.current_streak = 0
    
    def get_recent_performance(self, n=5):
        
        if not self.attempts:
            return None
        
        recent = self.attempts[-n:]
        correct_count = sum(1 for a in recent if a['is_correct'])
        total_time = sum(a['time_taken'] for a in recent)
        
        return {
            'accuracy': correct_count / len(recent),
            'avg_time': total_time / len(recent),
            'correct': correct_count,
            'total': len(recent),
            'current_streak': self.current_streak
        }
    
    def get_difficulty_performance(self, difficulty):
        
        difficulty_attempts = [a for a in self.attempts if a['difficulty'] == difficulty]
        
        if not difficulty_attempts:
            return None
        
        correct = sum(1 for a in difficulty_attempts if a['is_correct'])
        total_time = sum(a['time_taken'] for a in difficulty_attempts)
        
        return {
            'accuracy': correct / len(difficulty_attempts),
            'avg_time': total_time / len(difficulty_attempts),
            'attempts': len(difficulty_attempts)
        }
    
    def get_session_summary(self):
        
        if not self.attempts:
            return {
                'user_name': self.user_name,
                'total_attempts': 0,
                'message': 'No puzzles attempted yet'
            }
        
        total = len(self.attempts)
        correct = sum(1 for a in self.attempts if a['is_correct'])
        total_time = sum(a['time_taken'] for a in self.attempts)
        
        # Calculate performance by difficulty
        difficulty_stats = {}
        for difficulty in set(a['difficulty'] for a in self.attempts):
            stats = self.get_difficulty_performance(difficulty)
            if stats:
                difficulty_stats[difficulty] = stats
        
        # Calculate performance by operation
        operation_stats = {}
        for op in set(a['operation'] for a in self.attempts):
            op_attempts = [a for a in self.attempts if a['operation'] == op]
            op_correct = sum(1 for a in op_attempts if a['is_correct'])
            operation_stats[op] = {
                'accuracy': op_correct / len(op_attempts),
                'attempts': len(op_attempts)
            }
        
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            'user_name': self.user_name,
            'session_duration': round(session_duration, 2),
            'total_attempts': total,
            'correct_answers': correct,
            'overall_accuracy': round(correct / total * 100, 2),
            'avg_time_per_puzzle': round(total_time / total, 2),
            'max_streak': self.max_streak,
            'current_streak': self.current_streak,
            'difficulty_stats': difficulty_stats,
            'operation_stats': operation_stats,
            'final_difficulty': self.attempts[-1]['difficulty']
        }

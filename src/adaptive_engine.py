import numpy as np
from collections import deque

class AdaptiveEngine:
    def __init__(self, method='rule-based', window_size=5):
    
        self.method = method
        self.window_size = window_size
        self.difficulty_order = ['easy', 'medium', 'hard']
        self.performance_history = deque(maxlen=window_size)
        self.increase_threshold = 0.8  # 80% this increase difficulty
        self.decrease_threshold = 0.5  # >50% this decrease difficulty
        self.time_fast_threshold = 5.0  # seconds
        self.time_slow_threshold = 15.0  # seconds
        
    def recommend_difficulty(self, tracker, current_difficulty):
        
        if self.method == 'rule-based':
            return self._rule_based_recommendation(tracker, current_difficulty)
        elif self.method == 'ml-based':
            return self._ml_based_recommendation(tracker, current_difficulty)
        else:
            return current_difficulty, "Unknown method"
    
    def _rule_based_recommendation(self, tracker, current_difficulty):
        
        recent_perf = tracker.get_recent_performance(self.window_size)
        
        if not recent_perf:
            return current_difficulty, "Not enough data yet"
        
        accuracy = recent_perf['accuracy']
        avg_time = recent_perf['avg_time']
        streak = recent_perf['current_streak']
        
        current_idx = self.difficulty_order.index(current_difficulty)
        reasoning_parts = []
        
        # Primary factor: Accuracy
        if accuracy >= self.increase_threshold:
            reasoning_parts.append(f"High accuracy ({accuracy*100:.0f}%)")
            
            # Secondary factor: Time (only if accuracy is high)
            if avg_time < self.time_fast_threshold:
                reasoning_parts.append(f"Fast response time ({avg_time:.1f}s)")
                # Strong signal to increase difficulty
                if current_idx < len(self.difficulty_order) - 1:
                    new_difficulty = self.difficulty_order[current_idx + 1]
                    return new_difficulty, " + ".join(reasoning_parts) + " → Increase"
            elif streak >= 3:
                reasoning_parts.append(f"Good streak ({streak})")
                if current_idx < len(self.difficulty_order) - 1:
                    new_difficulty = self.difficulty_order[current_idx + 1]
                    return new_difficulty, " + ".join(reasoning_parts) + " → Increase"
            else:
                return current_difficulty, f"High accuracy but moderate speed → Maintain {current_difficulty}"
        
        elif accuracy <= self.decrease_threshold:
            reasoning_parts.append(f"Low accuracy ({accuracy*100:.0f}%)")
            
            # Check if time is also an issue
            if avg_time > self.time_slow_threshold:
                reasoning_parts.append(f"Slow response time ({avg_time:.1f}s)")
            
            if current_idx > 0:
                new_difficulty = self.difficulty_order[current_idx - 1]
                return new_difficulty, " + ".join(reasoning_parts) + " → Decrease"
            else:
                return current_difficulty, "Already at easiest level → Maintain"
        
        else:
            # Moderate performance - stay at current level
            return current_difficulty, f"Moderate accuracy ({accuracy*100:.0f}%) → Maintain {current_difficulty}"
    
    def _ml_based_recommendation(self, tracker, current_difficulty):
        
        recent_perf = tracker.get_recent_performance(self.window_size)
        
        if not recent_perf or len(tracker.attempts) < 3:
            return current_difficulty, "Collecting initial data"
        
        # Feature engineering
        accuracy = recent_perf['accuracy']
        avg_time = recent_perf['avg_time']
        streak = recent_perf['current_streak']
        
        # Normalize features (0-1 scale)
        accuracy_score = accuracy
        time_score = max(0, min(1, 1 - (avg_time - 5) / 15))  # Fast is good
        streak_score = min(1, streak / 5)  # Cap at 5
        
        # Weighted performance score
        # Accuracy is most important, followed by time, then streak
        performance_score = (0.6 * accuracy_score + 
                           0.25 * time_score + 
                           0.15 * streak_score)
        
        current_idx = self.difficulty_order.index(current_difficulty)
        
        # Dynamic thresholds based on current difficulty
        # Harder levels have stricter requirements to advance
        if current_difficulty == 'easy':
            increase_threshold = 0.7
            decrease_threshold = 0.4
        elif current_difficulty == 'medium':
            increase_threshold = 0.75
            decrease_threshold = 0.45
        else:  # hard
            increase_threshold = 0.8
            decrease_threshold = 0.5
        
        reasoning = f"ML Score: {performance_score:.2f} (Acc:{accuracy:.0%}, Time:{avg_time:.1f}s, Streak:{streak})"
        
        if performance_score >= increase_threshold and current_idx < len(self.difficulty_order) - 1:
            new_difficulty = self.difficulty_order[current_idx + 1]
            return new_difficulty, reasoning + " → Increase"
        elif performance_score <= decrease_threshold and current_idx > 0:
            new_difficulty = self.difficulty_order[current_idx - 1]
            return new_difficulty, reasoning + " → Decrease"
        else:
            return current_difficulty, reasoning + " → Maintain"
    
    def get_next_recommended_level(self, tracker):
        
        if not tracker.attempts:
            return 'easy'
        
        # Base recommendation on overall session performance
        summary = tracker.get_session_summary()
        overall_accuracy = summary['overall_accuracy'] / 100
        
        final_difficulty = summary['final_difficulty']
        current_idx = self.difficulty_order.index(final_difficulty)
        
        # If overall performance is strong, suggest maintaining or increasing
        if overall_accuracy >= 0.75:
            if current_idx < len(self.difficulty_order) - 1:
                return self.difficulty_order[current_idx + 1]
            return final_difficulty
        elif overall_accuracy < 0.5:
            if current_idx > 0:
                return self.difficulty_order[current_idx - 1]
            return 'easy'
        else:
            return final_difficulty

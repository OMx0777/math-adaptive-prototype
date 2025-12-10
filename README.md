Math Adventures - AI-Powered Adaptive Learning Prototype

An intelligent math learning system that dynamically adjusts puzzle difficulty based on real-time performance analysis.
Overview

Math Adventures is an adaptive learning prototype designed for children aged 5-10 to practice basic arithmetic. The system uses AI-powered algorithms to personalize the learning experience by automatically adjusting difficulty levels based on:

    Answer accuracy
    Response time
    Performance streaks
    Historical performance patterns

Architecture

┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                     (main.py)                           │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────────┐  ┌────▼─────────┐
│  Puzzle    │  │ Performance  │
│ Generator  │  │   Tracker    │
└───┬────────┘  └────┬─────────┘
    │                │
    │         ┌──────▼──────────┐
    └────────►│ Adaptive Engine │
              │  (Rule/ML Based)│
              └─────────────────┘

Components

    Puzzle Generator (puzzle_generator.py)
        Dynamically creates math problems
        Three difficulty levels: Easy, Medium, Hard
        Operations: Addition, Subtraction, Multiplication, Division
        Ensures age-appropriate number ranges
    Performance Tracker (tracker.py)
        Logs each attempt with timestamp
        Tracks accuracy, response time, and streaks
        Provides granular analytics by difficulty and operation
        Generates comprehensive session summaries
    Adaptive Engine (adaptive_engine.py)
        Rule-Based Mode: Uses threshold-based logic
            Primary factor: Recent accuracy (window of 5 attempts)
            Secondary factor: Response time
            Tertiary factor: Streak performance
        ML-Based Mode: Uses weighted performance scoring
            Feature engineering: accuracy (60%), time (25%), streak (15%)
            Dynamic thresholds based on current difficulty
        Real-time difficulty adjustment
    Main Application (main.py)
        Console-based interactive interface
        Session management and user flow
        Real-time feedback and progress visualization

Getting Started
Prerequisites
bash

Python 3.7+
numpy (for ML-based mode)

Installation

    Clone the repository:

bash

git clone https://github.com/yourusername/math-adaptive-prototype.git
cd math-adaptive-prototype

    Install dependencies:

bash

pip install -r requirements.txt

Running the Application
bash

python src/main.py

Adaptive Logic Explained
Rule-Based Approach

The rule-based engine uses a multi-factor decision system:

Difficulty Increase Conditions:

    Recent accuracy ≥ 80% AND
    (Average response time < 5s OR current streak ≥ 3)

Difficulty Decrease Conditions:

    Recent accuracy ≤ 50% OR
    (Recent accuracy < 60% AND average time > 15s)

Maintain Current Level:

    Performance between thresholds (50-80% accuracy)

ML-Based Approach

The ML approach uses a weighted performance scoring system:

Performance Score = 0.60 × Accuracy + 0.25 × Time_Score + 0.15 × Streak_Score

Where:
- Time_Score = normalized response time (faster = higher score)
- Streak_Score = current streak capped at 5

Adaptive Thresholds:

    Easy → Medium: Score ≥ 0.70
    Medium → Hard: Score ≥ 0.75
    Hard → Maintain: Score ≥ 0.80
    Decrease: Score ≤ difficulty-dependent threshold

Why This Approach?

Advantages:

    Multi-dimensional: Considers multiple performance aspects
    Responsive: Adjusts within 3-5 attempts
    Gradual: Prevents sudden, frustrating jumps
    Personalized: Adapts to individual learning pace
    Transparent: Provides reasoning for adjustments

Trade-offs:

    Rule-based: Simple, interpretable, but less flexible
    ML-based: More nuanced, adaptable, but requires more data

Key Metrics Tracked

    Accuracy: Percentage of correct answers
    Response Time: Average time per puzzle
    Streak: Consecutive correct answers
    Difficulty Distribution: Performance across levels
    Operation Performance: Accuracy by math operation

Example Session Flow

1. User enters name → Selects initial difficulty (Easy/Medium/Hard)
2. User chooses adaptation method (Rule-based/ML-based)
3. System generates puzzle at current difficulty
4. User solves puzzle → System records time and correctness
5. After 3+ attempts, adaptive engine evaluates performance
6. System adjusts difficulty if needed (with explanation)
7. Repeat steps 3-6
8. End session → Display comprehensive summary

Project Structure

math-adaptive-prototype/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── technical_note.md        # Detailed technical documentation
├── src/
│   ├── main.py              # Main application entry point
│   ├── puzzle_generator.py  # Puzzle generation logic
│   ├── tracker.py           # Performance tracking system
│   └── adaptive_engine.py   # Adaptive difficulty algorithm
└── docs/
    └── architecture_diagram.png

Future Enhancements
Data Collection Strategy

    User Profiles: Store anonymized performance histories
    A/B Testing: Compare rule-based vs ML effectiveness
    Long-term Tracking: Monitor learning progress over weeks
    Difficulty Calibration: Fine-tune thresholds using real user data

Handling Noisy Data

    Moving Averages: Smooth out performance fluctuations
    Confidence Intervals: Require consistent performance before adjusting
    Outlier Detection: Ignore anomalous attempts (e.g., accidental wrong inputs)
    Minimum Attempts: Require sufficient data before making changes

Scaling Beyond Math

    Modular Design: Abstract puzzle generation for other subjects
    Subject Profiles: Different adaptation strategies per subject
    Cross-subject Analytics: Identify transferable skills
    Curriculum Mapping: Align with educational standards

Contributing

This is an assignment prototype, but suggestions for improvements are welcome!
License

MIT License - Feel free to use for educational purposes.
Author

Created as part of an adaptive learning internship assignment.

Note: This is a minimal prototype focused on demonstrating adaptive logic. Production systems would include:

    Database persistence
    User authentication
    Web/mobile interface
    More sophisticated ML models
    Comprehensive testing suite


# AI Task Priority Predictor

An intelligent system that learns from your completed tasks and predicts which new tasks you should do first based on your personal productivity patterns.

## 🎯 What It Does

This AI system:
- **Tracks** when you complete different types of tasks
- **Learns** your productivity patterns (morning person? deadline-driven?)
- **Automatically prioritizes** new tasks based on your habits
- **Provides reasoning** for each priority prediction

## 🚀 Quick Start

### Option 1: Simple Version (No Dependencies)
```bash
python3 simple_task_ai.py
```

### Option 2: Full Version (With ML)
```bash
# Install dependencies (if you have pip access)
pip install pandas scikit-learn matplotlib numpy

# Run the full version
python3 task_priority_ai.py
```

### Option 3: Web Interface
```bash
# Install all dependencies
pip install -r requirements.txt

# Run the web server
python3 api_server.py

# Visit http://localhost:5000
```

## 📊 Features

### Sample Data Generation
- Generates 50-100 realistic sample tasks
- Includes features like:
  - Task type (email, coding, meeting, personal, research, review)
  - Time of day (morning, afternoon, evening)
  - Deadline urgency (high, medium, low)
  - Completion order

### Rule-Based Priority System
- **Morning + Urgent** → HIGH priority
- **Email + Afternoon** → MEDIUM priority
- **Creative tasks + Morning** → HIGH priority
- **Evening tasks** → LOW priority

### Machine Learning (Full Version)
- Decision Tree classifier for priority prediction
- Pattern recognition from historical data
- Confidence scoring for predictions

### Pattern Analysis
- Task type preferences by time of day
- Priority distribution analysis
- Urgency vs Priority correlation
- Visualizations (full version)

## 🔧 How It Works

### 1. Data Collection
The system generates sample tasks with realistic patterns:
```python
task = {
    'task_type': 'email',
    'time_of_day': 'morning', 
    'urgency': 'high',
    'priority': 'HIGH'
}
```

### 2. Pattern Learning
The AI learns from your task completion patterns:
- Which task types you prefer at different times
- How urgency affects your priority decisions
- Your personal productivity rhythms

### 3. Priority Prediction
For new tasks, the system predicts priority based on:
- **Learned patterns** from historical data
- **Rule-based logic** for common scenarios
- **Confidence scoring** for prediction reliability

### 4. Reasoning
Each prediction includes reasoning:
```
Task: "Reply to client email"
Predicted Priority: HIGH (85% confidence)
Reason: High urgency task + Morning time slot (typically high productivity)
```

## 📈 Example Output

```
🤖 AI Task Priority Predictor
==================================================

📊 Generating sample task data...
Generated 100 sample tasks

🧠 Learning patterns from historical data...

=== Productivity Pattern Analysis ===

Task Type Preferences by Time of Day:

MORNING:
  email: 12
  coding: 8
  meeting: 6
  research: 5

AFTERNOON:
  email: 10
  coding: 7
  meeting: 8
  review: 4

=== Testing New Tasks ===

Task: Reply to client email
Predicted Priority: HIGH (85% confidence)
Reason: High urgency task + Morning time slot (typically high productivity)

Task: Code review
Predicted Priority: MEDIUM (72% confidence)
Reason: Based on learned patterns
```

## 🎨 Visualizations (Full Version)

The full version generates:
- Priority distribution charts
- Task type preferences by time of day
- Urgency vs Priority correlation
- Priority trends over completion order

## 📁 Files Generated

- `task_data.json` - Historical task data
- `task_predictions.json` - Prediction results
- `productivity_patterns.png` - Visualizations (full version)
- `task_predictions.csv` - CSV results (full version)

## 🧠 AI Learning Process

1. **Pattern Recognition**: Identifies recurring patterns in your task completion
2. **Feature Analysis**: Analyzes task type, time, urgency relationships
3. **Priority Mapping**: Maps patterns to priority levels
4. **Confidence Scoring**: Provides confidence levels for predictions
5. **Continuous Learning**: Updates patterns as new data is added

## 🔮 Future Enhancements

- **Real-time Learning**: Update patterns as you complete tasks
- **Personalization**: Adapt to individual productivity styles
- **Integration**: Connect with task management tools
- **Advanced ML**: Use more sophisticated algorithms
- **Time Series**: Consider temporal patterns and trends

## 🛠️ Technical Details

### Simple Version
- Pure Python (no external dependencies)
- Rule-based + pattern learning
- JSON data storage
- Lightweight and fast

### Full Version
- Pandas for data manipulation
- Scikit-learn for machine learning
- Matplotlib for visualizations
- Decision Tree classification

## 📝 Usage Examples

### Adding New Tasks
```python
new_task = {
    'description': 'Write project proposal',
    'task_type': 'coding',
    'time_of_day': 'morning',
    'urgency': 'high'
}

priority, confidence = ai.predict_priority(
    new_task['task_type'],
    new_task['time_of_day'], 
    new_task['urgency']
)
```

### Analyzing Patterns
```python
# Analyze your productivity patterns
ai.analyze_patterns(tasks)

# Get reasoning for predictions
reasoning = ai._get_reasoning('email', 'morning', 'high')
```

## 🎯 Key Benefits

1. **Personalized**: Learns your specific productivity patterns
2. **Intelligent**: Uses both rules and machine learning
3. **Transparent**: Provides reasoning for each prediction
4. **Adaptive**: Improves with more data
5. **Practical**: Easy to understand and use

## 🚀 Getting Started

1. **Clone or download** the project files
2. **Run the simple version** first: `python3 simple_task_ai.py`
3. **Try the full version** if you have the dependencies
4. **Experiment** with different task types and scenarios
5. **Customize** the rules and patterns for your needs

---

*Built for AI Ignite Week - Demonstrating practical AI applications for productivity enhancement!*

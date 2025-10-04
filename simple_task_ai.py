#!/usr/bin/env python3
"""
Simple AI Task Priority Predictor
A lightweight system that learns from completed tasks and predicts priority
without external dependencies (uses only Python standard library).
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import defaultdict, Counter

class SimpleTaskPriorityAI:
    def __init__(self):
        self.task_types = ['email', 'coding', 'meeting', 'personal', 'research', 'review']
        self.time_periods = ['morning', 'afternoon', 'evening']
        self.urgency_levels = ['high', 'medium', 'low']
        self.priority_levels = ['HIGH', 'MEDIUM', 'LOW']
        self.learned_patterns = defaultdict(lambda: defaultdict(int))
        self.task_history = []
        
    def generate_sample_data(self, num_tasks: int = 100) -> List[Dict]:
        """Generate sample task data with realistic patterns"""
        random.seed(42)
        tasks = []
        
        for i in range(num_tasks):
            # Generate task with some realistic patterns
            task_type = random.choices(self.task_types, weights=[25, 20, 15, 15, 15, 10])[0]
            time_of_day = random.choices(self.time_periods, weights=[40, 40, 20])[0]
            urgency = random.choices(self.urgency_levels, weights=[20, 50, 30])[0]
            
            # Create realistic priority patterns
            priority = self._calculate_rule_based_priority(task_type, time_of_day, urgency)
            
            # Add some noise to make it more realistic
            if random.random() < 0.15:  # 15% chance to override with random priority
                priority = random.choice(self.priority_levels)
            
            task = {
                'task_id': i + 1,
                'task_type': task_type,
                'time_of_day': time_of_day,
                'urgency': urgency,
                'priority': priority,
                'completion_order': i + 1,
                'created_date': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            }
            tasks.append(task)
            self.task_history.append(task)
        
        return tasks
    
    def _calculate_rule_based_priority(self, task_type: str, time_of_day: str, urgency: str) -> str:
        """Calculate priority based on simple rules"""
        # Morning person pattern: urgent tasks in morning get high priority
        if urgency == 'high' and time_of_day == 'morning':
            return 'HIGH'
        
        # Email tasks in afternoon get medium priority
        if task_type == 'email' and time_of_day == 'afternoon':
            return 'MEDIUM'
        
        # Creative tasks in morning get high priority
        if task_type in ['coding', 'research'] and time_of_day == 'morning':
            return 'HIGH'
        
        # Meetings in afternoon get medium priority
        if task_type == 'meeting' and time_of_day == 'afternoon':
            return 'MEDIUM'
        
        # Evening tasks generally get lower priority
        if time_of_day == 'evening':
            return 'LOW'
        
        # Default based on urgency
        if urgency == 'high':
            return 'HIGH'
        elif urgency == 'medium':
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def learn_patterns(self, tasks: List[Dict]):
        """Learn patterns from historical task data"""
        for task in tasks:
            # Learn task type patterns
            key = f"{task['task_type']}_{task['time_of_day']}_{task['urgency']}"
            self.learned_patterns[key][task['priority']] += 1
    
    def predict_priority(self, task_type: str, time_of_day: str, urgency: str) -> Dict[str, any]:
        """Predict priority for a new task using learned patterns"""
        key = f"{task_type}_{time_of_day}_{urgency}"
        
        if key in self.learned_patterns:
            # Use learned patterns
            pattern_counts = self.learned_patterns[key]
            total = sum(pattern_counts.values())
            
            if total > 0:
                # Find most common priority for this pattern
                most_common_priority = max(pattern_counts, key=pattern_counts.get)
                confidence = pattern_counts[most_common_priority] / total
                return {'priority': most_common_priority, 'confidence': confidence}
        
        # Fallback to rule-based prediction
        predicted_priority = self._calculate_rule_based_priority(task_type, time_of_day, urgency)
        return {'priority': predicted_priority, 'confidence': 0.6}  # Medium confidence for rule-based
    
    def analyze_patterns(self, tasks: List[Dict]):
        """Analyze productivity patterns from the data"""
        print("\n=== Productivity Pattern Analysis ===")
        
        # Count task types by time of day
        time_task_counts = defaultdict(lambda: defaultdict(int))
        for task in tasks:
            time_task_counts[task['time_of_day']][task['task_type']] += 1
        
        print("\nTask Type Preferences by Time of Day:")
        for time_period in self.time_periods:
            print(f"\n{time_period.upper()}:")
            for task_type, count in time_task_counts[time_period].items():
                print(f"  {task_type}: {count}")
        
        # Priority distribution
        priority_counts = Counter(task['priority'] for task in tasks)
        print(f"\nPriority Distribution:")
        for priority, count in priority_counts.items():
            print(f"  {priority}: {count}")
        
        # Urgency vs Priority correlation
        urgency_priority = defaultdict(lambda: defaultdict(int))
        for task in tasks:
            urgency_priority[task['urgency']][task['priority']] += 1
        
        print(f"\nUrgency vs Priority Correlation:")
        for urgency in self.urgency_levels:
            print(f"\n{urgency.upper()} urgency:")
            for priority, count in urgency_priority[urgency].items():
                print(f"  {priority}: {count}")
    
    def test_new_tasks(self, new_tasks: List[Dict]) -> List[Dict]:
        """Test the system with new tasks"""
        print("\n=== Testing New Tasks ===")
        
        results = []
        for task in new_tasks:
            try:
                prediction = self.predict_priority(
                    task['task_type'], 
                    task['time_of_day'], 
                    task['urgency']
                )
                priority = prediction['priority']
                confidence = prediction['confidence']
                
                result = {
                    'task_description': task['description'],
                    'task_type': task['task_type'],
                    'time_of_day': task['time_of_day'],
                    'urgency': task['urgency'],
                    'predicted_priority': priority,
                    'confidence': f"{confidence:.1%}"
                }
                results.append(result)
                
                print(f"\nTask: {task['description']}")
                print(f"Predicted Priority: {priority} ({confidence:.1%} confidence)")
                print(f"Reason: {self._get_reasoning(task['task_type'], task['time_of_day'], task['urgency'])}")
                
            except Exception as e:
                print(f"Error predicting for task '{task['description']}': {e}")
        
        return results
    
    def _get_reasoning(self, task_type: str, time_of_day: str, urgency: str) -> str:
        """Provide reasoning for the prediction"""
        reasons = []
        
        if urgency == 'high':
            reasons.append("High urgency task")
        if time_of_day == 'morning':
            reasons.append("Morning time slot (typically high productivity)")
        if task_type in ['coding', 'research']:
            reasons.append("Creative/technical task")
        if task_type == 'email':
            reasons.append("Communication task")
        
        if not reasons:
            reasons.append("Based on learned patterns")
        
        return " + ".join(reasons)
    
    def save_data(self, filename: str = "task_data.json"):
        """Save task data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.task_history, f, indent=2)
        print(f"Task data saved to {filename}")
    
    def load_data(self, filename: str = "task_data.json"):
        """Load task data from JSON file"""
        try:
            with open(filename, 'r') as f:
                self.task_history = json.load(f)
            print(f"Task data loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"No existing data file found: {filename}")
            return False


def main():
    """Main function to demonstrate the AI system"""
    print("🤖 Simple AI Task Priority Predictor")
    print("=" * 50)
    
    # Initialize the AI system
    ai = SimpleTaskPriorityAI()
    
    # Generate sample data
    print("\n📊 Generating sample task data...")
    tasks = ai.generate_sample_data(100)
    print(f"Generated {len(tasks)} sample tasks")
    
    # Learn patterns from the data
    print("\n🧠 Learning patterns from historical data...")
    ai.learn_patterns(tasks)
    
    # Analyze patterns
    ai.analyze_patterns(tasks)
    
    # Test with new tasks
    new_tasks = [
        {
            'description': 'Reply to client email',
            'task_type': 'email',
            'time_of_day': 'morning',
            'urgency': 'high'
        },
        {
            'description': 'Code review',
            'task_type': 'review',
            'time_of_day': 'afternoon',
            'urgency': 'medium'
        },
        {
            'description': 'Research new technology',
            'task_type': 'research',
            'time_of_day': 'morning',
            'urgency': 'low'
        },
        {
            'description': 'Team standup meeting',
            'task_type': 'meeting',
            'time_of_day': 'morning',
            'urgency': 'high'
        },
        {
            'description': 'Update documentation',
            'task_type': 'coding',
            'time_of_day': 'afternoon',
            'urgency': 'medium'
        }
    ]
    
    # Test predictions
    results = ai.test_new_tasks(new_tasks)
    
    # Save data for future use
    ai.save_data("task_data.json")
    
    # Save results
    with open("task_predictions.json", 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to task_predictions.json")
    
    print("\n✅ Simple AI Task Priority Predictor demonstration complete!")
    print("Check the generated files:")
    print("- task_data.json (historical task data)")
    print("- task_predictions.json (prediction results)")


if __name__ == "__main__":
    main()

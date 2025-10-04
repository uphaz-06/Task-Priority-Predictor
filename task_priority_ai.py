#!/usr/bin/env python3
"""
AI Task Priority Predictor
A system that learns from completed tasks and predicts priority for new tasks
based on personal productivity patterns.
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
from typing import List, Dict, Tuple

class TaskPriorityAI:
    def __init__(self):
        self.model = None
        self.feature_columns = ['task_type_encoded', 'time_of_day_encoded', 'urgency_encoded']
        self.task_types = ['email', 'coding', 'meeting', 'personal', 'research', 'review']
        self.time_periods = ['morning', 'afternoon', 'evening']
        self.urgency_levels = ['high', 'medium', 'low']
        self.priority_levels = ['HIGH', 'MEDIUM', 'LOW']
        
    def generate_sample_data(self, num_tasks: int = 100) -> pd.DataFrame:
        """Generate sample task data with realistic patterns"""
        np.random.seed(42)
        random.seed(42)
        
        tasks = []
        
        for i in range(num_tasks):
            # Generate task with some realistic patterns
            task_type = np.random.choice(self.task_types, p=[0.25, 0.2, 0.15, 0.15, 0.15, 0.1])
            time_of_day = np.random.choice(self.time_periods, p=[0.4, 0.4, 0.2])  # More morning/afternoon
            urgency = np.random.choice(self.urgency_levels, p=[0.2, 0.5, 0.3])
            
            # Create realistic priority patterns
            priority = self._calculate_rule_based_priority(task_type, time_of_day, urgency)
            
            # Add some noise to make it more realistic
            if np.random.random() < 0.15:  # 15% chance to override with random priority
                priority = np.random.choice(self.priority_levels)
            
            # Generate completion order (simulate realistic task ordering)
            completion_order = i + 1
            
            # Add some features that might affect priority
            is_deadline_driven = urgency == 'high'
            is_creative_task = task_type in ['coding', 'research']
            is_communication = task_type in ['email', 'meeting']
            
            task = {
                'task_id': i + 1,
                'task_type': task_type,
                'time_of_day': time_of_day,
                'urgency': urgency,
                'priority': priority,
                'completion_order': completion_order,
                'is_deadline_driven': is_deadline_driven,
                'is_creative_task': is_creative_task,
                'is_communication': is_communication,
                'created_date': datetime.now() - timedelta(days=random.randint(1, 30))
            }
            tasks.append(task)
        
        return pd.DataFrame(tasks)
    
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
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for machine learning"""
        df_encoded = df.copy()
        
        # Encode categorical variables
        task_type_mapping = {task: i for i, task in enumerate(self.task_types)}
        time_mapping = {time: i for i, time in enumerate(self.time_periods)}
        urgency_mapping = {urgency: i for i, urgency in enumerate(self.urgency_levels)}
        
        df_encoded['task_type_encoded'] = df_encoded['task_type'].map(task_type_mapping)
        df_encoded['time_of_day_encoded'] = df_encoded['time_of_day'].map(time_mapping)
        df_encoded['urgency_encoded'] = df_encoded['urgency'].map(urgency_mapping)
        
        return df_encoded
    
    def train_model(self, df: pd.DataFrame):
        """Train the decision tree model"""
        df_encoded = self.prepare_features(df)
        
        X = df_encoded[self.feature_columns]
        y = df_encoded['priority']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        self.model = DecisionTreeClassifier(random_state=42, max_depth=5)
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.2f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return self.model
    
    def predict_priority(self, task_type: str, time_of_day: str, urgency: str) -> Tuple[str, float]:
        """Predict priority for a new task"""
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model() first.")
        
        # Encode the input
        task_type_mapping = {task: i for i, task in enumerate(self.task_types)}
        time_mapping = {time: i for i, time in enumerate(self.time_periods)}
        urgency_mapping = {urgency: i for i, urgency in enumerate(self.urgency_levels)}
        
        features = np.array([[
            task_type_mapping[task_type],
            time_mapping[time_of_day],
            urgency_mapping[urgency]
        ]])
        
        # Get prediction and confidence
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = max(probabilities)
        
        return prediction, confidence
    
    def analyze_patterns(self, df: pd.DataFrame):
        """Analyze productivity patterns from the data"""
        print("\n=== Productivity Pattern Analysis ===")
        
        # Task type preferences by time of day
        print("\nTask Type Preferences by Time of Day:")
        time_task_prefs = df.groupby(['time_of_day', 'task_type']).size().unstack(fill_value=0)
        print(time_task_prefs)
        
        # Priority patterns
        print("\nPriority Distribution:")
        priority_dist = df['priority'].value_counts()
        print(priority_dist)
        
        # Urgency vs Priority correlation
        print("\nUrgency vs Priority Correlation:")
        urgency_priority = pd.crosstab(df['urgency'], df['priority'])
        print(urgency_priority)
        
        # Time of day preferences
        print("\nTime of Day Preferences:")
        time_prefs = df['time_of_day'].value_counts()
        print(time_prefs)
    
    def visualize_patterns(self, df: pd.DataFrame):
        """Create visualizations of productivity patterns"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Priority distribution
        df['priority'].value_counts().plot(kind='bar', ax=axes[0, 0], color='skyblue')
        axes[0, 0].set_title('Priority Distribution')
        axes[0, 0].set_xlabel('Priority Level')
        axes[0, 0].set_ylabel('Count')
        
        # Task type by time of day
        time_task = df.groupby(['time_of_day', 'task_type']).size().unstack(fill_value=0)
        time_task.plot(kind='bar', ax=axes[0, 1], stacked=True)
        axes[0, 1].set_title('Task Types by Time of Day')
        axes[0, 1].set_xlabel('Time of Day')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Urgency vs Priority
        urgency_priority = pd.crosstab(df['urgency'], df['priority'])
        urgency_priority.plot(kind='bar', ax=axes[1, 0], color=['red', 'orange', 'green'])
        axes[1, 0].set_title('Urgency vs Priority')
        axes[1, 0].set_xlabel('Urgency Level')
        axes[1, 0].set_ylabel('Count')
        axes[1, 0].legend(title='Priority')
        
        # Completion order over time
        df_sorted = df.sort_values('completion_order')
        axes[1, 1].plot(df_sorted['completion_order'], df_sorted['priority'].map({'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}), 'o-')
        axes[1, 1].set_title('Priority Trend Over Completion Order')
        axes[1, 1].set_xlabel('Completion Order')
        axes[1, 1].set_ylabel('Priority Level')
        axes[1, 1].set_yticks([1, 2, 3])
        axes[1, 1].set_yticklabels(['LOW', 'MEDIUM', 'HIGH'])
        
        plt.tight_layout()
        plt.savefig('/home/lenovo/Desktop/AI Ignite Week/productivity_patterns.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def test_new_tasks(self, new_tasks: List[Dict]) -> pd.DataFrame:
        """Test the system with new tasks"""
        print("\n=== Testing New Tasks ===")
        
        results = []
        for task in new_tasks:
            try:
                priority, confidence = self.predict_priority(
                    task['task_type'], 
                    task['time_of_day'], 
                    task['urgency']
                )
                
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
        
        return pd.DataFrame(results)
    
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


def main():
    """Main function to demonstrate the AI system"""
    print("🤖 AI Task Priority Predictor")
    print("=" * 50)
    
    # Initialize the AI system
    ai = TaskPriorityAI()
    
    # Generate sample data
    print("\n📊 Generating sample task data...")
    df = ai.generate_sample_data(100)
    print(f"Generated {len(df)} sample tasks")
    
    # Analyze patterns
    ai.analyze_patterns(df)
    
    # Train the model
    print("\n🧠 Training AI model...")
    ai.train_model(df)
    
    # Create visualizations
    print("\n📈 Creating visualizations...")
    ai.visualize_patterns(df)
    
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
    results_df = ai.test_new_tasks(new_tasks)
    
    # Save results
    results_df.to_csv('/home/lenovo/Desktop/AI Ignite Week/task_predictions.csv', index=False)
    print(f"\n💾 Results saved to task_predictions.csv")
    
    print("\n✅ AI Task Priority Predictor demonstration complete!")
    print("Check the generated files:")
    print("- productivity_patterns.png (visualizations)")
    print("- task_predictions.csv (prediction results)")


if __name__ == "__main__":
    main()

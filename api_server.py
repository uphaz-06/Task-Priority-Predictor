#!/usr/bin/env python3
"""
Simple API Server for AI Task Priority Predictor
Provides REST API endpoints for the web interface
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import subprocess
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Import our AI system
from simple_task_ai import SimpleTaskPriorityAI

# Initialize the AI system
ai_system = SimpleTaskPriorityAI()

# Load existing data or generate sample data
if os.path.exists('task_data.json'):
    with open('task_data.json', 'r') as f:
        ai_system.task_history = json.load(f)
    ai_system.learn_patterns(ai_system.task_history)
    print(f"Loaded {len(ai_system.task_history)} historical tasks")
else:
    print("No existing data found, generating sample data...")
    tasks = ai_system.generate_sample_data(100)
    ai_system.learn_patterns(tasks)
    ai_system.save_data("task_data.json")

@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', filename)

@app.route('/api/predict', methods=['POST'])
def predict_priority():
    """Predict task priority"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['task_type', 'time_of_day', 'urgency']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get prediction
        prediction = ai_system.predict_priority(
            data['task_type'],
            data['time_of_day'],
            data['urgency']
        )
        
        # Get reasoning
        reasoning = ai_system._get_reasoning(
            data['task_type'],
            data['time_of_day'],
            data['urgency']
        )
        
        # Add to history
        new_task = {
            'task_id': len(ai_system.task_history) + 1,
            'task_type': data['task_type'],
            'time_of_day': data['time_of_day'],
            'urgency': data['urgency'],
            'priority': prediction['priority'],
            'completion_order': len(ai_system.task_history) + 1,
            'created_date': datetime.now().isoformat()
        }
        
        ai_system.task_history.append(new_task)
        ai_system.learn_patterns(ai_system.task_history)
        ai_system.save_data("task_data.json")
        
        return jsonify({
            'success': True,
            'prediction': {
                'priority': prediction['priority'],
                'confidence': prediction['confidence'],
                'reasoning': reasoning
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data"""
    try:
        # Calculate analytics from task history
        analytics = {
            'total_tasks': len(ai_system.task_history),
            'priority_distribution': {},
            'time_distribution': {},
            'task_type_distribution': {},
            'urgency_distribution': {}
        }
        
        # Count distributions
        for task in ai_system.task_history:
            # Priority distribution
            priority = task['priority']
            analytics['priority_distribution'][priority] = analytics['priority_distribution'].get(priority, 0) + 1
            
            # Time distribution
            time_of_day = task['time_of_day']
            analytics['time_distribution'][time_of_day] = analytics['time_distribution'].get(time_of_day, 0) + 1
            
            # Task type distribution
            task_type = task['task_type']
            analytics['task_type_distribution'][task_type] = analytics['task_type_distribution'].get(task_type, 0) + 1
            
            # Urgency distribution
            urgency = task['urgency']
            analytics['urgency_distribution'][urgency] = analytics['urgency_distribution'].get(urgency, 0) + 1
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    """Get learned patterns"""
    try:
        return jsonify({
            'success': True,
            'patterns': ai_system.learned_patterns,
            'task_types': ai_system.task_types,
            'time_periods': ai_system.time_periods,
            'urgency_levels': ai_system.urgency_levels,
            'priority_levels': ai_system.priority_levels
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        return jsonify({
            'success': True,
            'tasks': ai_system.task_history[-50:]  # Return last 50 tasks
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Add a new task"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['task_type', 'time_of_day', 'urgency', 'priority']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new task
        new_task = {
            'task_id': len(ai_system.task_history) + 1,
            'task_type': data['task_type'],
            'time_of_day': data['time_of_day'],
            'urgency': data['urgency'],
            'priority': data['priority'],
            'completion_order': len(ai_system.task_history) + 1,
            'created_date': datetime.now().isoformat()
        }
        
        ai_system.task_history.append(new_task)
        ai_system.learn_patterns(ai_system.task_history)
        ai_system.save_data("task_data.json")
        
        return jsonify({
            'success': True,
            'task': new_task
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_tasks': len(ai_system.task_history)
    })

@app.route('/api/reset', methods=['POST'])
def reset_data():
    """Reset all data (for testing)"""
    try:
        # Generate new sample data
        tasks = ai_system.generate_sample_data(100)
        ai_system.learn_patterns(tasks)
        ai_system.save_data("task_data.json")
        
        return jsonify({
            'success': True,
            'message': 'Data reset successfully',
            'total_tasks': len(ai_system.task_history)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Task Priority Predictor API Server...")
    print("📊 Loaded AI system with task data")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📱 Web interface: http://localhost:5000")
    print("🔗 API endpoints:")
    print("  - POST /api/predict - Predict task priority")
    print("  - GET  /api/analytics - Get analytics data")
    print("  - GET  /api/patterns - Get learned patterns")
    print("  - GET  /api/tasks - Get all tasks")
    print("  - POST /api/tasks - Add new task")
    print("  - GET  /api/health - Health check")
    print("  - POST /api/reset - Reset data")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

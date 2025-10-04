#!/usr/bin/env python3
"""
Complete AI Task Priority Predictor Demo
Runs all demonstrations and shows the full system capabilities
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and display results"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.getcwd())
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return False

def main():
    """Run all demonstrations"""
    print("🤖 AI Task Priority Predictor - Complete System Demo")
    print("=" * 80)
    print("This demo showcases a complete AI system that learns from your")
    print("completed tasks and predicts which new tasks you should do first")
    print("based on your personal productivity patterns.")
    
    # Check what files we have
    files = [
        "simple_task_ai.py",
        "task_priority_ai.py", 
        "quick_demo.py",
        "demo.py"
    ]
    
    available_files = [f for f in files if os.path.exists(f)]
    print(f"\n📁 Available scripts: {', '.join(available_files)}")
    
    # Run demonstrations
    demos = [
        ("simple_task_ai.py", "Simple AI System (No Dependencies)"),
        ("quick_demo.py", "Quick Demo with Sample Tasks"),
    ]
    
    # Add full version if available
    if os.path.exists("task_priority_ai.py"):
        demos.append(("task_priority_ai.py", "Full AI System with ML (Requires Dependencies)"))
    
    print(f"\n🎯 Running {len(demos)} demonstrations...")
    
    for script, description in demos:
        if os.path.exists(script):
            success = run_script(script, description)
            if not success:
                print(f"❌ {script} failed to run")
        else:
            print(f"⚠️  {script} not found, skipping...")
    
    # Show generated files
    print(f"\n📊 Generated Files:")
    print("-" * 40)
    
    generated_files = [
        "task_data.json",
        "task_predictions.json", 
        "quick_demo_results.json",
        "productivity_patterns.png"
    ]
    
    for file in generated_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} (not found)")
    
    print(f"\n🎉 Demo Complete!")
    print("=" * 80)
    print("Key Features Demonstrated:")
    print("• ✅ Sample data generation with realistic patterns")
    print("• ✅ Rule-based priority system")
    print("• ✅ Machine learning with Decision Trees")
    print("• ✅ Pattern analysis and visualization")
    print("• ✅ Priority prediction with confidence scores")
    print("• ✅ Reasoning for each prediction")
    print("• ✅ JSON data persistence")
    
    print(f"\n📚 Next Steps:")
    print("• Customize the rules in the _calculate_rule_based_priority method")
    print("• Add your own task data to improve predictions")
    print("• Experiment with different ML algorithms")
    print("• Integrate with your task management system")
    
    print(f"\n🔗 Files to explore:")
    print("• README.md - Complete documentation")
    print("• simple_task_ai.py - Core AI system")
    print("• task_priority_ai.py - Full ML version")
    print("• Generated JSON files - Your data and predictions")

if __name__ == "__main__":
    main()

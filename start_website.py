#!/usr/bin/env python3
"""
Startup script for the AI Task Priority Predictor Website
Launches both the API server and opens the web browser
"""

import subprocess
import sys
import time
import webbrowser
import os
from threading import Thread

def start_api_server():
    """Start the Flask API server"""
    print("🚀 Starting API server...")
    try:
        subprocess.run([sys.executable, 'api_server.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 API server stopped")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")

def open_browser():
    """Open the web browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    print("🌐 Opening web browser...")
    webbrowser.open('http://localhost:5000')

def main():
    """Main startup function"""
    print("🤖 AI Task Priority Predictor - Website Launcher")
    print("=" * 60)
    
    # Check if required files exist
    required_files = ['index.html', 'styles.css', 'script_api.js', 'api_server.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please make sure all website files are present.")
        return
    
    print("✅ All required files found")
    print("📁 Website files:")
    print("  - index.html (main page)")
    print("  - styles.css (styling)")
    print("  - script_api.js (JavaScript with API integration)")
    print("  - api_server.py (Flask API server)")
    
    print("\n🚀 Starting the website...")
    print("📡 API server will run on: http://localhost:5000")
    print("🌐 Website will be available at: http://localhost:5000")
    print("\n💡 Features:")
    print("  • Interactive task prediction")
    print("  • Real-time analytics")
    print("  • AI-powered priority suggestions")
    print("  • Beautiful responsive design")
    print("  • REST API integration")
    
    print("\n🎯 Starting services...")
    
    # Start browser in a separate thread
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the API server (this will block)
    try:
        start_api_server()
    except KeyboardInterrupt:
        print("\n👋 Website stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

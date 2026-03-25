"""Launcher script for DOE Simulator Streamlit application."""
import sys
import os

try:
    import streamlit.cli
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(script_dir, 'app.py')
    
    print(f"Starting DOE Simulator...")
    print(f"App file: {app_file}")
    print(f"App exists: {os.path.exists(app_file)}")
    
    # Set up sys.argv for streamlit
    sys.argv = ['streamlit', 'run', app_file]
    
    # Run streamlit
    print("Launching Streamlit...")
    streamlit.cli.main()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")



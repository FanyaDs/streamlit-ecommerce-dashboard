import os
import sys

# Add the dashboard directory to the path so we can import modules if needed
sys.path.append(os.path.join(os.path.dirname(__file__), 'dashboard'))

# Import the dashboard logic
# If dashboard.py has a main function or just runs on import, we can execute it here.
# For Streamlit, the easiest is to just run the command, but since we are one file,
# let's just copy the content or use 'exec'.

with open(os.path.join(os.path.dirname(__file__), 'dashboard', 'dashboard.py'), 'r', encoding='utf-8') as f:
    exec(f.read())

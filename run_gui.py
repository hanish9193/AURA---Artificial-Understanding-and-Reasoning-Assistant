"""
Launch AURA Tkinter GUI with sample data
"""

from aura import Aura
import pandas as pd
import tempfile
import os

# Create sample data
data = pd.DataFrame({
    'Age': [25, 30, 35, 40, 45, 50, 55, 60],
    'Income': [30000, 35000, 42000, 55000, 65000, 75000, 85000, 95000],
    'Experience': [2, 5, 8, 12, 15, 20, 25, 30],
    'Satisfaction': [6, 7, 7, 8, 8, 9, 9, 8],
})

# Use tempfile for cross-platform compatibility
temp_dir = tempfile.gettempdir()
sample_data_path = os.path.join(temp_dir, 'sample_data.csv')
data.to_csv(sample_data_path, index=False)

# Use AURA
print("🚀 AURA - Launching Tkinter GUI\n")

aura = Aura()
aura.load_data(sample_data_path)
aura.generate_insights()

# Launch the interactive Tkinter GUI
print("\n🎨 Opening Tkinter GUI window...")
aura.launch_gui()


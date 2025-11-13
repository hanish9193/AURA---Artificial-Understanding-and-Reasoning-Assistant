"""
Quick start example - 2 minute setup
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
print("🚀 AURA Quick Start\n")

aura = Aura()
aura.load_data(sample_data_path)

insights = aura.generate_insights()
print(f"\n📊 Insights: {insights}\n")

# Ask questions
questions = [
    "What correlations exist?",
    "Are there any missing values?",
    "What's the data quality?",
    "Identify any flaws in the data",
    "What are the most important features?"
]

for q in questions:
    print(f"\n❓ {q}")
    print(f"{'='*50}")
    print(aura.ask(q))

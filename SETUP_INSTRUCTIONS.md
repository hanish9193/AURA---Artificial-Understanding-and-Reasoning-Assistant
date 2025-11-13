# AURA Setup Instructions

## Step 1: Create Virtual Environment
\`\`\`bash
conda create -n aura_env python=3.11
conda activate aura_env
\`\`\`

## Step 2: Install Dependencies (Windows Compatible)
\`\`\`bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
\`\`\`

**If you still get errors:**
\`\`\`bash
# Option A: Use pre-built wheels only (no compilation)
pip install --only-binary :all: -r requirements.txt

# Option B: Install one at a time with verbose output
pip install pandas numpy matplotlib seaborn scikit-learn pillow tensorflow
\`\`\`

## Step 3: Test Installation
\`\`\`bash
python examples/quick_start.py
\`\`\`

You should see:
- CSV file loaded
- 15 graphs generated in `/outputs` folder
- Q&A responses for data insights
- NO training happening (only pre-trained model)

## Step 4: Use AURA in Your Project
\`\`\`python
from aura import Aura

aura = Aura()
aura.load_data("your_data.csv")
aura.generate_insights()  # Generates 15 graphs
aura.open_gui()  # Launches Tkinter chatbot GUI
\`\`\`

The Tkinter GUI will appear with Q&A chatbot interface.

## Troubleshooting
- **numpy build error**: Delete environment and recreate with `python=3.10`
- **tensorflow issues**: Use `tensorflow-cpu` instead if GPU not available
- **Memory issues**: Use `aura.load_data("file.csv", sample=True)` for large datasets

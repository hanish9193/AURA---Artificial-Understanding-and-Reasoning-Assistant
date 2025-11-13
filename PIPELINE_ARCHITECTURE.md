# AURA Pipeline Architecture

## Complete Flow

### 1. **Data Loading** 
- Load CSV data
- Validate (min 2 numeric columns)

### 2. **Graph Generation**
- Generate 15 visualizations (correlations, distributions, outliers, etc.)
- Save as PNG bytes

### 3. **Feature Extraction (EfficientNetB0)**
- Pre-trained CNN extracts **1280-D embeddings** from each graph
- No training required - uses ImageNet weights
- Output: (15, 1280) embedding matrix

### 4. **VisionTextBridge (Neural Module)** ⭐ KEY STEP
- Takes 1280-D embeddings as INPUT
- Projects to 4096-D semantic space (learned)
- Predicts visual attributes:
  - Trend (negative/flat/positive)
  - Density (sparse/clustered/dense)
  - Outliers (present/absent)
  - Shape (uniform/skewed/bimodal/irregular)
- **Outputs**: Natural language descriptions like:
  - "Visual pattern: positive trend, dense data, no outliers, uniform distribution"
  
### 5. **Mistral LLM Q&A** 
- Receives:
  - Dataset statistics (shape, columns, missing data)
  - Graph metadata (names, types)
  - **VisionTextBridge descriptions** (TEXT from embeddings)
- Processes user questions with full context
- Returns intelligent, context-aware answers

## Why This Works

1. **Embeddings capture visual patterns** - CNN learns what graphs look like
2. **VisionTextBridge translates to text** - Neural bridge converts numbers → meaning
3. **Mistral understands text + data** - LLM reason about insights
4. **No API needed** - All models run locally offline

## Running the Pipeline

\`\`\`bash
# 1. Train VisionTextBridge (once)
python scripts/train_vision_bridge.py

# 2. Run AURA
python examples/quick_start.py

# 3. Or use direct API
from aura import Aura
aura = Aura()
aura.load_data("data.csv")
aura.generate_insights()  # Runs full pipeline
aura.launch_gui()  # Interactive Tkinter GUI

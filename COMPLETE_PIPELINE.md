# AURA: Complete Neural Pipeline for Data Intelligence

## System Architecture

### 1. Data Input
- User provides CSV file
- AURA validates data quality

### 2. Visualization Layer
- **GraphGenerator** creates 15 diverse graphs:
  - Correlation matrices (relationships)
  - Distributions (data spread)
  - Scatter plots (variable relationships)
  - Box plots (outlier detection)
  - Category plots (categorical analysis)
  - Data quality visualization
  - Feature importance

### 3. Computer Vision Layer (CNN)
- **EfficientNetB0** pre-trained model
- Converts graph images → 1280-dimensional embeddings
- Captures visual patterns: correlations, trends, densities, outliers
- No training required (pre-trained on ImageNet)

### 4. Vision-to-Language Bridge (Neural)
- **VisionTextBridge**: Neural module (supervised training)
- Input: 1280-D embeddings from CNN
- Process:
  - Project embeddings to 4096-D semantic space
  - Classify visual attributes:
    - Trend (negative/flat/positive)
    - Density (sparse/clustered/dense)
    - Outliers (present/absent)
    - Shape (uniform/skewed/bimodal/irregular)
  - Convert classifications → natural language descriptions
- Output: Human-readable text describing graph patterns
- Training: Uses CrossEntropyLoss with supervised labels

### 5. Large Language Model Layer
- **Mistral-7B LLM** (local, offline)
- Input: Text descriptions from VisionTextBridge + user questions
- Process:
  - Understands data patterns from bridge descriptions
  - Learns correlations, trends, and insights
  - Generates contextual, intelligent responses
- Output: Natural language answers about data

### 6. Interactive User Interface
- **Tkinter GUI** for Q&A interaction
- Displays chat history
- Real-time responses powered by Mistral

## Complete Data Flow

\`\`\`
CSV Data
  ↓
[15 Graphs Generated]
  ↓
[EfficientNetB0 - Visual Feature Extraction]
  ↓
[1280-D Embeddings per Graph]
  ↓
[VisionTextBridge - Neural Bridge]
  ↓
[Graph Descriptions + Insights]
  ↓
[Mistral-7B LLM Context]
  ↓
[User Questions + LLM Processing]
  ↓
[Intelligent Q&A Responses]
\`\`\`

## Key Innovation: Why This Works

1. **Multi-Modal Analysis**: Combines visual (graphs) + semantic (embeddings) + linguistic (LLM)
2. **No API Dependencies**: Fully offline, runs locally
3. **Context-Aware Q&A**: Mistral understands data patterns from VisionTextBridge descriptions
4. **Supervised Learning**: VisionTextBridge learns what patterns mean through supervised training
5. **Scalable**: Works with any CSV data

## Usage

\`\`\`python
from aura import Aura

aura = Aura()
aura.load_data("data.csv")
aura.generate_insights()
aura.launch_gui()  # Interactive Q&A session
\`\`\`

## Component Details

### VisionTextBridge Training
- Converts visual embeddings → semantic text
- Supervised learning with CrossEntropyLoss
- Learns to classify and describe graph patterns
- Trained on synthetic data generated from actual graphs

### Mistral Integration
- Uses Ollama local server
- Context includes all graph descriptions
- Fallback mode with rule-based insights if Ollama unavailable
- Streaming responses for natural interaction

## Research Implications

- **Novel Approach**: First system to bridge CNN embeddings directly to LLM for data analysis
- **Autonomous Insights**: Model learns to extract meaning from visual patterns
- **Practical**: No manual feature engineering required
- **Reproducible**: Fully deterministic with seed-based randomization

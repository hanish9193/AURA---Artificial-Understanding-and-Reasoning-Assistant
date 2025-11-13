"""
Train VisionTextBridge on graph embeddings
Run this once to create the trained model
"""

import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from aura.vision_text_bridge import train_vision_text_bridge, save_model
from aura.graph_generator import GraphGenerator
from aura.feature_extractor import FeatureExtractor
import pandas as pd

# Example data
print("📊 Generating training data...")
data = pd.DataFrame({
    'A': np.random.randn(100),
    'B': np.random.randn(100) * 2 + 5,
    'C': np.random.randn(100) * 3
})

# Generate graphs
graph_gen = GraphGenerator(data)
graphs, metadata = graph_gen.create_all_graphs()

# Extract embeddings
extractor = FeatureExtractor()
embeddings = extractor.extract_features(graphs)

# Train bridge
model = train_vision_text_bridge(embeddings, epochs=10)

# Save
save_model(model, "models/vision_text_bridge.pt")

print("✓ VisionTextBridge trained and saved!")

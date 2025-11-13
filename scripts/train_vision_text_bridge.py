"""
Train the VisionTextBridge with REAL supervised labels from data analysis
"""

import sys
from pathlib import Path
import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).parent.parent))

from aura.graph_generator import GraphGenerator
from aura.feature_extractor import FeatureExtractor
from aura.vision_text_bridge import train_vision_text_bridge, save_model
from scripts.generate_training_labels import generate_dataset_labels
import pandas as pd


def main():
    print("=" * 70)
    print("AURA VisionTextBridge - Real Data-Driven Supervised Training")
    print("=" * 70)
    
    # Step 1: Create sample data
    print("\n1️⃣ Creating sample dataset...")
    np.random.seed(42)
    n_samples = 100
    data = pd.DataFrame({
        'A': np.random.randn(n_samples),
        'B': np.random.randn(n_samples) + np.linspace(0, 3, n_samples),  # Positive trend
        'C': np.random.exponential(2, n_samples),  # Skewed distribution
        'D': np.random.randint(0, 5, n_samples)
    })
    print(f"   ✓ Dataset shape: {data.shape}")
    
    # Step 2: Generate graphs
    print("\n2️⃣ Generating 15 graphs from data...")
    graph_gen = GraphGenerator(data)
    graphs, graph_metadata = graph_gen.create_all_graphs()
    print(f"   ✓ Created {len(graphs)} graphs")
    
    # Step 3: Extract embeddings
    print("\n3️⃣ Extracting embeddings with EfficientNetB0...")
    extractor = FeatureExtractor()
    embeddings = extractor.extract_features(graphs)
    print(f"   ✓ Extracted embeddings shape: {embeddings.shape}")
    
    print("\n4️⃣ Generating REAL ground-truth labels from data...")
    labels = generate_dataset_labels(data, graph_metadata)
    
    # Step 5: Train with supervised learning
    print("\n5️⃣ Training VisionTextBridge with supervision...")
    model = train_vision_text_bridge(
        embeddings=embeddings,
        labels=labels,
        epochs=20,
        device='cpu'
    )
    
    # Step 6: Save model
    print("\n6️⃣ Saving trained model...")
    save_model(model, "models/vision_text_bridge.pt")
    
    # Step 7: Test on sample embeddings
    print("\n7️⃣ Testing on sample embeddings...")
    for i in range(min(3, len(embeddings))):
        test_embedding = embeddings[i]
        description, semantic = model.describe_embedding(test_embedding, graph_metadata[i])
        print(f"   Graph {i+1}: {description}")
    
    print("\n" + "=" * 70)
    print("✓ Training complete! Model learned from REAL data patterns.")
    print("=" * 70)


if __name__ == "__main__":
    main()

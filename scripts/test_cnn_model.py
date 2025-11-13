"""
Test script to verify CNN (EfficientNetB7) pre-trained model loads correctly
"""

import sys
from pathlib import Path

# Add aura to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aura.feature_extractor import FeatureExtractor
import numpy as np
from PIL import Image
import io

def test_cnn_model():
    print("\n" + "="*60)
    print("🧠 TESTING CNN MODEL (EfficientNetB7)")
    print("="*60)
    
    try:
        # Step 1: Initialize
        print("\n[1/3] Initializing FeatureExtractor...")
        extractor = FeatureExtractor()
        
        if extractor.model is None:
            print("❌ FAILED: Model is None (TensorFlow not installed?)")
            return False
        
        print("✓ Model initialized successfully")
        print(f"   Model type: {type(extractor.model)}")
        print(f"   Model name: EfficientNetB7")
        
        # Step 2: Create dummy image
        print("\n[2/3] Creating test image...")
        img = Image.new('RGB', (224, 224), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        print(f"✓ Test image created: {len(img_bytes)} bytes")
        
        # Step 3: Extract features
        print("\n[3/3] Extracting features from image...")
        embeddings = extractor.extract_features([img_bytes])
        
        print(f"✓ Features extracted successfully")
        print(f"   Shape: {embeddings.shape}")
        print(f"   Expected: (1, 1280)")
        print(f"   Data type: {embeddings.dtype}")
        print(f"   Sample values: {embeddings[0][:5]}")
        
        # Verification
        if embeddings.shape == (1, 1280):
            print("\n✅ CNN MODEL TEST PASSED!")
            return True
        else:
            print(f"\n❌ FAILED: Wrong shape {embeddings.shape}, expected (1, 1280)")
            return False
    
    except ImportError as e:
        print(f"\n❌ FAILED: Import error - {e}")
        print("   Make sure TensorFlow is installed: pip install tensorflow")
        return False
    
    except Exception as e:
        print(f"\n❌ FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cnn_model()
    sys.exit(0 if success else 1)

"""
Test script to verify NLP Q&A engine works correctly
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add aura to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aura.qa_engine import QAEngine

def test_nlp_model():
    print("\n" + "="*60)
    print("🧠 TESTING NLP Q&A ENGINE")
    print("="*60)
    
    try:
        # Step 1: Initialize
        print("\n[1/4] Initializing QAEngine...")
        qa = QAEngine()
        print("✓ QAEngine initialized")
        
        # Step 2: Create test data
        print("\n[2/4] Creating test dataset...")
        test_data = pd.DataFrame({
            'age': [25, 30, 35, 40, 45, 50],
            'salary': [30000, 45000, 50000, 60000, 70000, 80000],
            'experience': [1, 3, 5, 8, 10, 12],
            'missing_col': [1, 2, np.nan, 4, 5, 6],
        })
        print(f"✓ Test data created:")
        print(test_data)
        
        # Step 3: Prepare Q&A engine
        print("\n[3/4] Preparing Q&A engine...")
        graph_metadata = [
            {"title": "Correlation Matrix", "type": "heatmap"},
            {"title": "Age Distribution", "type": "histogram"},
        ]
        dummy_embeddings = np.random.rand(2, 1280)
        
        qa.prepare(test_data, graph_metadata, dummy_embeddings)
        print("✓ Q&A engine prepared with test data")
        
        # Step 4: Test questions
        print("\n[4/4] Testing Q&A responses...")
        test_questions = [
            "What correlations exist?",
            "Show missing data",
            "What is data quality?",
            "Identify flaws",
            "Find outliers",
        ]
        
        print("\n" + "-"*60)
        all_passed = True
        for question in test_questions:
            try:
                response = qa.answer(question)
                if response and len(response) > 0:
                    print(f"\n✓ Q: {question}")
                    print(f"  A: {response[:80]}...")
                else:
                    print(f"\n❌ Q: {question} - Empty response")
                    all_passed = False
            except Exception as e:
                print(f"\n❌ Q: {question} - Error: {e}")
                all_passed = False
        
        if all_passed:
            print("\n✅ NLP Q&A ENGINE TEST PASSED!")
            return True
        else:
            print("\n❌ Some Q&A tests failed")
            return False
    
    except ImportError as e:
        print(f"\n❌ FAILED: Import error - {e}")
        return False
    
    except Exception as e:
        print(f"\n❌ FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_nlp_model()
    sys.exit(0 if success else 1)

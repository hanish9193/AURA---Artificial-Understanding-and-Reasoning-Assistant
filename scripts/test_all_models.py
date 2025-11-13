"""
Master test script - Run both CNN and NLP tests
"""

import sys
import subprocess
from pathlib import Path

def run_test(script_name):
    """Run a test script and return result"""
    script_path = Path(__file__).parent / script_name
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}")
    
    result = subprocess.run([sys.executable, str(script_path)], capture_output=False)
    return result.returncode == 0

def main():
    print("\n" + "#"*60)
    print("# AURA MODEL VERIFICATION SUITE")
    print("#"*60)
    
    results = {
        "CNN Model (EfficientNetB7)": run_test("test_cnn_model.py"),
        "NLP Q&A Engine": run_test("test_nlp_model.py"),
    }
    
    print("\n" + "#"*60)
    print("# FINAL RESULTS")
    print("#"*60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("#"*60)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Your models are ready.\n")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED. Fix issues before running AURA.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

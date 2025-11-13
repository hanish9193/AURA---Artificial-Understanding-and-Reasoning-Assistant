"""
Run the complete AURA project:
1. Load sample data
2. Generate 15+ graphs
3. Extract visual features
4. Launch interactive Tkinter GUI
"""

from aura import Aura
import pandas as pd
import tempfile
import os
import sys

def main():
    print("=" * 70)
    print("AURA - Advanced Unified Relationship Analyzer")
    print("Full Project Execution")
    print("=" * 70)
    
    # Create sample data
    print("\n📊 Step 1: Creating sample dataset...")
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
    print(f"✓ Sample data created: {sample_data_path}")
    
    # Initialize AURA
    print("\n🚀 Step 2: Initializing AURA...")
    aura = Aura()
    
    # Load data
    print("\n📥 Step 3: Loading data...")
    aura.load_data(sample_data_path)
    
    # Generate insights (graphs + embeddings)
    print("\n🔍 Step 4: Generating insights (graphs + embeddings)...")
    insights = aura.generate_insights()
    print(f"\n✓ Generated {insights['total_graphs']} graphs")
    print(f"✓ Data shape: {insights['data_shape']}")
    print(f"✓ Numeric columns: {insights['numeric_columns']}")
    
    # Show data flaws
    print("\n🔎 Step 5: Analyzing data quality...")
    flaws = aura.get_data_flaws()
    print(f"✓ Duplicates: {flaws['duplicates']}")
    print(f"✓ Missing values: {sum(flaws['missing_values'].values())}")
    
    # Launch GUI
    print("\n🎨 Step 6: Launching interactive Tkinter GUI...")
    print("=" * 70)
    print("The GUI window should open now!")
    print("You can:")
    print("  - Ask questions about your data")
    print("  - View generated graphs")
    print("  - Interact with AI-powered Q&A")
    print("=" * 70)
    print("\nPress Ctrl+C to exit when done.\n")
    
    try:
        aura.launch_gui()
    except KeyboardInterrupt:
        print("\n\n✓ GUI closed. Project execution complete!")
    except Exception as e:
        print(f"\n❌ Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


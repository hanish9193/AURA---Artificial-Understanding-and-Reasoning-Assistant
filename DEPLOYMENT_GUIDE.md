# AURA - Step-by-Step Verification & PyPI Upload Guide

## STEP 1: Verify Local Installation & Test

### 1.1 Install Dependencies
\`\`\`bash
cd aura
pip install -r requirements.txt
\`\`\`

### 1.2 Test the Core Library (No Streamlit)
\`\`\`bash
python examples/quick_start.py
\`\`\`

**✅ What you should see:**
- Data loaded: "8 rows, 4 columns"
- 15 graphs generated (check `/outputs` folder)
- Pre-trained model downloads **once** (TensorFlow cache)
- Q&A answers about correlations, missing data, quality, flaws, outliers
- **NO training happens** - just embeddings from pre-trained EfficientNetB7

### 1.3 Check Generated Artifacts
\`\`\`bash
ls -la outputs/  # Should have 15 graph PNG files
\`\`\`

---

## STEP 2: Test Streamlit Interactive App

### 2.1 Install Streamlit
\`\`\`bash
pip install streamlit
\`\`\`

### 2.2 Run the App
\`\`\`bash
streamlit run app.py
\`\`\`

### 2.3 Test in Browser
- Upload `examples/sample_data.csv` (or any CSV)
- Verify graphs load
- Test Q&A: "What correlations exist?"
- Check `/outputs` folder for saved graphs

**✅ Expected behavior:**
- File uploads successfully
- Data preview shows
- Q&A responds correctly
- Graphs saved to disk

---

## STEP 3: Prepare for PyPI

### 3.1 Verify setup.py
Check that `setup.py` has:
- ✅ Correct name: `aura-viz`
- ✅ Correct version: `1.0.0`
- ✅ All dependencies listed
- ✅ Author & description filled in

\`\`\`bash
cat setup.py
\`\`\`

### 3.2 Create Required Files
\`\`\`bash
# Create README
echo "# AURA - Advanced Data Visualizer" > README.md

# Create LICENSE
echo "MIT License" > LICENSE.txt

# Create version file
touch __init__.py
\`\`\`

### 3.3 Build Distribution
\`\`\`bash
pip install build twine

# Build wheel & source distribution
python -m build

# Check distribution
ls -la dist/
\`\`\`

**✅ You should see:**
- `aura_viz-1.0.0-py3-none-any.whl`
- `aura-viz-1.0.0.tar.gz`

---

## STEP 4: Upload to PyPI (Test First!)

### 4.1 Register on TestPyPI
1. Go to https://test.pypi.org/account/register/
2. Create account & generate API token
3. Save token safely

### 4.2 Create `.pypirc` Config
\`\`\`bash
cat > ~/.pypirc << EOF
[testpypi]
  repository = https://test.pypi.org/legacy/
  username = __token__
  password = pypi-AgEIcHlwaS5vcmc... (your token)

[pypi]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = pypi-AgEIcHlwaS5vcmc... (your production token)
EOF

chmod 600 ~/.pypirc
\`\`\`

### 4.3 Upload to TestPyPI First
\`\`\`bash
twine upload --repository testpypi dist/*
\`\`\`

**✅ Success message:**
\`\`\`
Uploading aura_viz-1.0.0-py3-none-any.whl [100%]
Uploading aura-viz-1.0.0.tar.gz [100%]
View your upload at: https://test.pypi.org/project/aura-viz/
\`\`\`

### 4.4 Test Installation from TestPyPI
\`\`\`bash
pip install --index-url https://test.pypi.org/simple/ aura-viz
python -c "from aura import Aura; print('✓ AURA imported successfully!')"
\`\`\`

---

## STEP 5: Upload to Production PyPI

### 5.1 Generate Production Token
1. Go to https://pypi.org/account/
2. Create new API token
3. Save to `.pypirc`

### 5.2 Upload to Production
\`\`\`bash
twine upload dist/*
\`\`\`

### 5.3 Verify Installation
\`\`\`bash
pip install aura-viz
python -c "from aura import Aura; aura = Aura(); print('✓ AURA ready!')"
\`\`\`

### 5.4 View on PyPI
- Visit: https://pypi.org/project/aura-viz/
- Users can now install: `pip install aura-viz`

---

## STEP 6: Usage Instructions for End Users

Once published, users can:

\`\`\`python
from aura import Aura

aura = Aura()
aura.load_data("their_data.csv")
aura.generate_insights()
answer = aura.ask("What correlations exist?")
print(answer)
\`\`\`

Or with Streamlit:
\`\`\`bash
pip install streamlit
streamlit run app.py
\`\`\`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `No module named 'aura'` | Run `pip install -r requirements.txt` in project root |
| TensorFlow download fails | Check internet, may take 5-10 min first time |
| Streamlit port error | Run `streamlit run app.py --server.port 8501` |
| PyPI upload fails | Check `.pypirc` permissions: `chmod 600 ~/.pypirc` |
| Import errors in test | Ensure you're in project root, not `aura/` folder |

---

## Checklist Before Production

- [ ] Local testing passes (`python examples/quick_start.py`)
- [ ] Streamlit app works
- [ ] TestPyPI upload successful
- [ ] TestPyPI installation works
- [ ] setup.py metadata is correct
- [ ] README.md is complete
- [ ] All dependencies pinned in setup.py
- [ ] License file included
- [ ] Version bumped in `__init__.py` and `setup.py`

**Ready to ship!** 🚀

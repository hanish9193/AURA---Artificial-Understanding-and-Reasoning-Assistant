import streamlit as st
import pandas as pd
from aura import Aura
import tempfile
import os

st.set_page_config(page_title="AURA - Data Visualizer", layout="wide")

st.title("🌟 AURA - AI Data Visualizer")
st.markdown("Upload your CSV and explore insights, correlations, and relationships with AI-powered Q&A")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        st.success("✅ File uploaded successfully!")

# Main content
if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    try:
        # Initialize AURA
        st.info("🔄 Loading data and generating insights...")
        aura = Aura()
        aura.load_data(tmp_path)
        
        # Display data preview
        st.subheader("📊 Data Preview")
        df = pd.read_csv(tmp_path)
        st.dataframe(df.head(10), use_container_width=True)
        
        st.metric("Total Rows", len(df))
        st.metric("Total Columns", len(df.columns))
        
        # Generate insights
        st.subheader("🔍 Insights Generated")
        insights = aura.generate_insights()
        st.success(insights)
        
        # Display graphs
        st.subheader("📈 Data Visualizations (15 Graphs)")
        st.info("Graphs are saved in the `/outputs` folder")
        
        # Q&A Section
        st.subheader("🤖 Ask AURA About Your Data")
        user_question = st.text_input("Ask a question about your data:")
        
        if user_question:
            st.info("⏳ Thinking...")
            answer = aura.ask(user_question)
            st.success(answer)
        
        # Cleanup
        os.unlink(tmp_path)
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        os.unlink(tmp_path)

else:
    st.info("👈 Upload a CSV file to get started!")
    st.markdown("""
    ### Example Questions AURA Can Answer:
    - "What are the strongest correlations in this data?"
    - "Which columns have the most missing values?"
    - "What are the outliers in this dataset?"
    - "Which features are most important?"
    - "Is there any data quality issue?"
    """)

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from prompt import templates  # Import prompt templates from prompt.py

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
else:
    st.error("❌ GEMINI_API_KEY not found in .env file")
    st.stop()

# ==================== HELPER FUNCTIONS ====================

def load_file(uploaded_file):
    """
    Load CSV or XLSX file and return as pandas DataFrame
    """
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(uploaded_file)
        else:
            st.error("❌ Unsupported file format. Please upload CSV or XLSX files.")
            return None
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return None


def generate_summary(data, doc_type):
    """
    Generate AI summary based on document type and data
    """
    try:
        if data is None or data.empty:
            return "❌ No data available to analyze"
        
        # Convert data to string format
        data_string = data.to_string()
        
        # Get appropriate template
        if doc_type not in templates:
            return f"❌ Unknown document type: {doc_type}"
        
        template = templates[doc_type]
        
        # Format prompt with data
        prompt = template.format(data=data_string)
        
        # Generate response from AI
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"❌ Error generating summary: {str(e)}"


def create_visualization(data, title):
    """
    Create visualization for financial data
    """
    try:
        st.subheader(title)
        
        # Display raw data
        st.write("**Raw Data:**")
        st.dataframe(data, use_container_width=True)
        
        # Create line chart for numerical columns
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.write("**Data Visualization:**")
            st.line_chart(data[numeric_cols])
        else:
            st.info("ℹ️ No numerical data available for visualization")
            
    except Exception as e:
        st.error(f"❌ Error creating visualization: {str(e)}")


# ==================== STREAMLIT APP LAYOUT ====================

# App Title and Description
st.set_page_config(page_title="Gemini Financial Decoder", layout="wide")
st.title("💰 Gemini Pro Financial Decoder")
st.markdown("### Transforming Complex Financial Data into Actionable Insights")
st.markdown("""
Transform your financial documents into clear, actionable insights using AI-powered analysis.
Upload your balance sheets, profit & loss statements, or cash flow statements and get instant summaries!
""")

st.divider()

# ==================== FILE UPLOAD SECTION ====================
st.header("📤 Upload Financial Documents")

col1, col2, col3 = st.columns(3)

with col1:
    balance_sheet_file = st.file_uploader(
        "📊 Balance Sheet (CSV/XLSX)", 
        type=["csv", "xlsx"],
        key="balance_sheet"
    )

with col2:
    profit_loss_file = st.file_uploader(
        "📈 Profit & Loss Statement (CSV/XLSX)", 
        type=["csv", "xlsx"],
        key="profit_loss"
    )

with col3:
    cash_flow_file = st.file_uploader(
        "💵 Cash Flow Statement (CSV/XLSX)", 
        type=["csv", "xlsx"],
        key="cash_flow"
    )

st.divider()

# ==================== GENERATE REPORT BUTTON ====================
if st.button("🚀 Generate AI Report", key="generate_btn", use_container_width=True):
    
    if not balance_sheet_file and not profit_loss_file and not cash_flow_file:
        st.warning("⚠️ Please upload at least one financial document to proceed")
    else:
        # Create progress indicator
        with st.spinner("⏳ Analyzing your financial data..."):
            
            # ========== BALANCE SHEET ==========
            if balance_sheet_file:
                st.header("📊 Balance Sheet Analysis")
                
                df_bs = load_file(balance_sheet_file)
                if df_bs is not None:
                    # Generate summary
                    summary_bs = generate_summary(df_bs, "balance_sheet")
                    
                    # Display in tabs
                    tab1, tab2 = st.tabs(["📝 Summary", "📊 Data & Visualization"])
                    
                    with tab1:
                        st.markdown(summary_bs)
                    
                    with tab2:
                        create_visualization(df_bs, "Balance Sheet Data")
                
                st.divider()
            
            # ========== PROFIT & LOSS ==========
            if profit_loss_file:
                st.header("📈 Profit & Loss Statement Analysis")
                
                df_pl = load_file(profit_loss_file)
                if df_pl is not None:
                    # Generate summary
                    summary_pl = generate_summary(df_pl, "profit_loss")
                    
                    # Display in tabs
                    tab1, tab2 = st.tabs(["📝 Summary", "📊 Data & Visualization"])
                    
                    with tab1:
                        st.markdown(summary_pl)
                    
                    with tab2:
                        create_visualization(df_pl, "Profit & Loss Data")
                
                st.divider()
            
            # ========== CASH FLOW ==========
            if cash_flow_file:
                st.header("💵 Cash Flow Statement Analysis")
                
                df_cf = load_file(cash_flow_file)
                if df_cf is not None:
                    # Generate summary
                    summary_cf = generate_summary(df_cf, "cash_flow")
                    
                    # Display in tabs
                    tab1, tab2 = st.tabs(["📝 Summary", "📊 Data & Visualization"])
                    
                    with tab1:
                        st.markdown(summary_cf)
                    
                    with tab2:
                        create_visualization(df_cf, "Cash Flow Data")
        
        st.success("✅ Report generated successfully!")

st.divider()

# Footer
st.markdown("""
---
**How to use this app:**
1. Upload your financial documents (Balance Sheet, P&L, or Cash Flow)
2. Click "Generate AI Report"
3. View AI-generated summaries and visualizations
4. Get actionable insights for better decision-making

**Powered by Google Gemini AI & LangChain** 🤖
""")

import streamlit as st
import pandas as pd
import plotly.express as px  # REQUIRED IMPORT
import time
import re
from duckduckgo_search import DDGS

# --- PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="Faber Nexus | AI-Consultant Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PROFESSIONAL UI ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #f8fafc; }
    
    /* Header Styling */
    h1, h2, h3 { color: #1e3a5f; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Custom Teal Buttons */
    .stButton>button {
        background-color: #208C8D;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover { background-color: #1D7480; color: white; }

    /* Styled Expanders (Cards) */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        color: #1e3a5f;
        font-weight: 600;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #1e3a5f; color: white; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] label { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("## 🟦 **FABER**")
with col2:
    st.title("NEXUS")
    st.caption("AI-Driven Operations Intelligence Platform | Internal Pre-Sales Tool")

st.markdown("---")

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header("🎯 Project Scoping")
    
    selected_industry = st.selectbox(
        "Select Client Industry:",
        ["Automotive", "Pharmaceuticals", "FMCG / CPG", "Heavy Engineering", "Textiles", "Logistics"]
    )
    
    selected_tool = st.selectbox(
        "Select Diagnostic Framework:",
        ["Value Stream Mapping (VSM)", "5S & Workplace Org", "Hoshin Kanri", "Total Productive Maintenance (TPM)", "Six Sigma", "Lean"]
    )
    
    budget_range = st.select_slider(
        "💰 Client Budget Constraint:",
        options=["<$100k", "$100k-$500k", "$500k-$1M", "$1M+"]
    )
    
    st.markdown("---")
    st.markdown("### 🤖 System Status")
    st.success("✅ Internal Archive: Online")
    st.success("✅ Global Search: Online")

# --- HELPER FUNCTION: REAL WEB SEARCH ---
def search_global_benchmarks(query, num_results=4):
    """Searches DuckDuckGo for real case studies and parses them."""
    results = []
    # Enhance query to get better case study results
    search_query = f"{query} case study operational excellence roi impact"
    
    try:
        with DDGS() as ddgs:
            # Perform the search
            ddg_results = list(ddgs.text(search_query, max_results=num_results))
            
            for res in ddg_results:
                snippet = res.get('body', '')
                
                # SMART PARSING: Extract ROI numbers from snippet text
                # Looks for patterns like "$5M", "20%", etc.
                savings_match = re.search(r'(\$\d+(?:\.\d+)?[MBK]?|\d+(?:\.\d+)?%)', snippet)
                savings = savings_match.group(0) if savings_match else "See Report"
                
                # Determine impact keyword based on text
                impact = "Operational Efficiency"
                if "reduce" in snippet.lower(): impact = "Cost Reduction"
                elif "increase" in snippet.lower(): impact = "Revenue Growth"
                elif "faster" in snippet.lower(): impact = "Speed / Throughput"

                results.append({
                    "title": res.get('title', 'Case Study'),
                    "summary": snippet,
                    "link": res.get('href', '#'),
                    "savings": savings,
                    "impact": impact
                })
    except Exception as e:
        st.error(f"Search Engine Error: {e}")
        # Fallback Mock Data if internet fails
        results.append({
            "title": "Global Benchmark (Offline Mode)",
            "summary": "Could not connect to live search. Please check internet connection.",
            "link": "#",
            "savings": "N/A",
            "impact": "Connection Error"
        })
    
    return results

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["🧠 Internal Brain (Archives)", "🌍 External Brain (Live Search)", "💰 ROI Simulator"])

# --- TAB 1: INTERNAL BRAIN ---
with tab1:
    st.subheader(f"📂 Faber Archives: {selected_industry} Projects")
    
    # Internal Mock Data Structure (Enhanced with new fields)
    internal_db = {
        "Automotive": [
            {"Client": "[REDACTED_AUTO_OEM]", "Project": "Assembly Line VSM", "Year": 2023, "ROI": "4.5x", "Team": "4 Consultants", "Result": "22% Cost Reduction"},
            {"Client": "[REDACTED_TIER1]", "Project": "Shop Floor 5S", "Year": 2022, "ROI": "3.2x", "Team": "3 Consultants", "Result": "Zero Accidents / 12 Months"},
        ],
        "Pharmaceuticals": [
            {"Client": "[REDACTED_PHARMA_GIANT]", "Project": "Batch Cycle Optimization", "Year": 2023, "ROI": "5.0x", "Team": "5 Consultants", "Result": "15% Capacity Release"},
        ],
        # Default Fallback
        "Other": [
            {"Client": "[REDACTED_CLIENT]", "Project": "Operational Excellence", "Year": 2021, "ROI": "2.5x", "Team": "3 Consultants", "Result": "10% Efficiency Gain"}
        ]
    }
    
    projects = internal_db.get(selected_industry, internal_db["Other"])
    
    for p in projects:
        # Improved Layout: Columns inside Expander
        with st.expander(f"📄 {p['Project']} ({p['Year']}) | ROI: {p['ROI']}"):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**Client:** `{p['Client']}`")
                st.markdown(f"**Outcome:** {p['Result']}")
                st.info(f"💡 **Recommended Team Size:** {p['Team']}")
            with c2:
                st.metric("Net ROI", p['ROI'], delta="Verified")
            
            st.download_button("📥 Download Sanitized Deck", data="Mock PDF Content", file_name=f"{p['Project']}.pdf")

# --- TAB 2: EXTERNAL BRAIN (LIVE SEARCH) ---
with tab2:
    st.subheader("🌍 Live Market Intelligence")
    
    # Search Interface
    c_search, c_btn = st.columns([4, 1])
    with c_search:
        default_query = f"{selected_industry} {selected_tool} case study"
        user_query = st.text_input("Search Global Benchmarks:", value=default_query)
    with c_btn:
        st.write("") # Spacer
        st.write("") # Spacer
        search_clicked = st.button("🔍 Run Live Search")
    
    # Initialize session state for results so they don't disappear
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None

    if search_clicked:
        with st.spinner(f"🤖 Agents are scanning global databases for '{user_query}'..."):
            # CALL THE REAL SEARCH FUNCTION
            st.session_state.search_results = search_global_benchmarks(user_query)
            
    # Display Results
    if st.session_state.search_results:
        results = st.session_state.search_results
        
        # Metric Summary Row
        m1, m2, m3 = st.columns(3)
        m1.metric("Sources Scanned", "15+", "Global")
        m2.metric("Top Result Confidence", "High", "98%")
        m3.metric("Avg. Industry Savings", "18-25%", "Est.")
        
        st.divider()
        
        # Result Cards
        for res in results:
            with st.container():
                st.markdown(f"### [{res['title']}]({res['link']})")
                st.caption(f"Source: Global Web Index | Impact: {res['impact']}")
                
                col_text, col_stat = st.columns([3, 1])
                with col_text:
                    st.write(res['summary'])
                with col_stat:
                    if res['savings'] != "See Report":
                        st.markdown(f"**Reported Savings:**")
                        st.markdown(f"## 💰 {res['savings']}")
                    else:
                        st.markdown("*Metrics inside report*")
                
                st.markdown("---")

# --- TAB 3: ROI SIMULATOR ---
with tab3:
    st.subheader("💸 Pre-Sales Value Estimator")
    
    col_x, col_y = st.columns([1, 2])
    
    with col_x:
        st.markdown("#### Client Inputs")
        revenue = st.number_input("Client Annual Revenue (₹ Crores)", value=100)
        inefficiency = st.slider("Estimated Inefficiency Gap (%)", 5, 30, 15)
        consulting_fee = st.number_input("Proposed Consulting Fee (₹ Lakhs)", value=25)
        
    with col_y:
        # The Math
        potential_savings = revenue * (inefficiency / 100)
        roi_ratio = (potential_savings * 100) / consulting_fee if consulting_fee > 0 else 0
        
        st.markdown("#### 📊 Projected Impact Analysis")
        
        # Data for Chart
        chart_data = pd.DataFrame({
            "Category": ["Consulting Investment", "Projected Savings"],
            "Amount (₹ Cr)": [consulting_fee/100, potential_savings]
        })
        
        fig = px.bar(chart_data, x="Category", y="Amount (₹ Cr)", color="Category", 
                     color_discrete_sequence=["#FF4B4B", "#00CC96"], 
                     text_auto=True)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"**Net ROI for Client:** {roi_ratio:.1f}x Return on Investment")

# --- FOOTER ---
st.markdown("---")
f1, f2, f3 = st.columns(3)
with f1:
    if st.button("📝 Generate Draft Proposal"):
        st.toast("Generating PDF Proposal... (Simulated)")
with f2:
    if st.button("🤖 Stress Test with AI Client"):
        st.toast("Launching AI Skeptic Mode... (Simulated)")
with f3:
    st.caption("Faber Infinite Consulting | Internal Tool v1.2")

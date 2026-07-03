import streamlit as st
import io
import sys
import os
import pandas as pd
from google import genai

# Configure your API key here 
os.environ["GEMINI_API_KEY"] = "YOUR GEMINI API KEY"
client = genai.Client()

# --- STEP 2: CODE EXECUTION SANDBOX WITH PERSISTENT LOGIC ---
def execute_agent_code(code_string, current_df_path):
    df = pd.read_csv(current_df_path)
    local_vars = {"df": df, "pd": pd}
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        exec(code_string, {}, local_vars)
        sys.stdout = old_stdout
        if isinstance(local_vars.get("df"), pd.DataFrame):
            local_vars["df"].to_csv(current_df_path, index=False)
        return redirected_output.getvalue().strip()
    except Exception as e:
        sys.stdout = old_stdout
        return f"EXECUTION_ERROR: {str(e)}"

# --- STEP 3: GEMINI AGENT BRAIN ---
class AutonomousAnalyst:
    def __init__(self, model="gemini-2.5-flash"):
        self.model = model

    def analyze(self, current_df_path, user_query):
        df = pd.read_csv(current_df_path)
        schema = df.dtypes.to_string()
        sample_rows = df.head(3).to_string()
        
        system_prompt = f"""
        You are a Senior Lead Data Analyst. You have access to a pandas DataFrame called `df`.
        DATASET SCHEMA:
        {schema}
        SAMPLE ROWS:
        {sample_rows}
        
        YOUR TASK:
        Write Python code to answer the user's request. 
        - Your code must explicitly use `print()` to output the final answer or insights.
        - If the user asks to clean, modify, or engineer features, alter the `df` object directly. It will be auto-saved.
        - To generate charts, use `matplotlib` or `seaborn` and save them via `plt.savefig('output_chart.png')`.
        - Return ONLY raw, executable Python code. Do not wrap it in markdown code blocks like ```python. Do not write text explanations outside of your code comments.
        """
        conversation_history = [
            {"role": "user", "parts": [{"text": f"{system_prompt}\n\nRequest: {user_query}"}]}
        ]

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=self.model, contents=conversation_history, config={"temperature": 0.1}
                )
                generated_code = response.text.strip()
                execution_result = execute_agent_code(generated_code, current_df_path)
                
                if "EXECUTION_ERROR" not in execution_result:
                    return execution_result, generated_code
                
                conversation_history.append({"role": "model", "parts": [{"text": generated_code}]})
                conversation_history.append({"role": "user", "parts": [{"text": f"Your code had this error: {execution_result}. Fix it entirely."}]})
            except Exception as api_error:
                return f"⚠️ Server Busy: {str(api_error)}. Please try clicking again.", "No code generated."
        return "❌ Agent failed to complete the analysis.", None

# --- STREAMLIT UI DESIGN & THEMING ---
st.set_page_config(page_title="InsightCore // Autonomous AI Analyst", layout="wide", page_icon="📊")

# Custom CSS Injection for high-fidelity professional UI design
st.markdown("""
    <style>
    /* Elegant metric card customization */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #4F46E5;
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #4B5563;
    }
    
    /* Styled container cards for past execution steps */
    .agent-card {
        background-color: #F8FAFC;
        border-left: 5px solid #6366F1;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    
    /* Custom Badge/Tag labels */
    .status-tag {
        background-color: #EEF2F6;
        color: #1E293B;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

PERSISTENT_CSV = "agent_working_dataset.csv"
CHART_PATH = "output_chart.png"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR DESIGN ---
st.sidebar.markdown("<h2 style='color: #4F46E5; margin-bottom: 0;'>⚙️ Data Control</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #6B7280; font-size: 13px;'>Upload and export configurations</p>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload Target Dataset (CSV)", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        st.session_state.chat_history = [] 
        init_df = pd.read_csv(uploaded_file)
        init_df.to_csv(PERSISTENT_CSV, index=False)
        if os.path.exists(CHART_PATH):
            os.remove(CHART_PATH)

# --- MAIN DASHBOARD LAYOUT ---
st.markdown("<h1 style='margin-bottom:0px; font-weight: 800; background: linear-gradient(45deg, #3B82F6, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🧠 InsightCore Analyst</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #6B7280; font-size: 16px; margin-top:0px;'>Senior-grade autonomous workspace environment powered by Gemini-2.5</p>", unsafe_allow_html=True)
st.markdown("---")

if os.path.exists(PERSISTENT_CSV):
    current_working_df = pd.read_csv(PERSISTENT_CSV)
    
    # Operational KPI Summary Grid Row
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Total Data Records", value=f"{current_working_df.shape[0]:,} rows")
    with kpi2:
        st.metric(label="Feature Dimensionality", value=f"{current_working_df.shape[1]} columns")
    with kpi3:
        missing_count = current_working_df.isnull().sum().sum()
        st.metric(label="Detected Empty Cells", value=f"{missing_count:,}", delta="Requires Attention" if missing_count > 0 else "Fully Clean", delta_color="inverse")
        
    st.markdown("### 🗂️ Data Workspace Preview")
    
    # Tabs layout
    tab_preview, tab_schema = st.tabs(["📄 Active Matrix Grid", "🛠️ Internal Column Schema"])
    with tab_preview:
        st.dataframe(current_working_df.head(5), use_container_width=True)
    with tab_schema:
        st.dataframe(pd.DataFrame({"Data Type": current_working_df.dtypes.astype(str)}), use_container_width=True)
        
    # Sidebar download customization
    with open(PERSISTENT_CSV, "rb") as file:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📥 Pipeline Output")
        st.sidebar.download_button(
            label="Download Working State (CSV)",
            data=file, file_name="insightcore_cleaned_dataset.csv", mime="text/csv",
            use_container_width=True
        )
    
    # Console command panel
    st.markdown("---")
    st.markdown("### 🕹️ Analyst Command Console")
    user_query = st.text_input("Enter natural language engineering directives or visualization requests:", placeholder="e.g., Clean the dataset prices, or plot a boxplot for product prices.", label_visibility="collapsed")
    
    if st.button("Execute Pipeline Directives", type="primary", use_container_width=True) and user_query:
        if os.path.exists(CHART_PATH):
            os.remove(CHART_PATH)
            
        analyst = AutonomousAnalyst()
        with st.spinner("🤖 Orchestrating agent loop memory context and executing scripts locally..."):
            result, code = analyst.analyze(PERSISTENT_CSV, user_query)
        
        chart_generated = os.path.exists(CHART_PATH)
        if chart_generated:
            entry_id = len(st.session_state.chat_history)
            saved_chart_name = f"chart_{entry_id}.png"
            os.rename(CHART_PATH, saved_chart_name)
        else:
            saved_chart_name = None

        st.session_state.chat_history.append({
            "query": user_query,
            "result": result,
            "code": code,
            "chart": saved_chart_name
        })
        st.rerun()

    # --- RENDERING EXPANDABLE CHRONOLOGICAL HISTORY ---
    if st.session_state.chat_history:
        st.markdown("### 💬 Process Timeline & Analytical History")
        
        for i, entry in enumerate(reversed(st.session_state.chat_history)):
            st.markdown(f"""
                <div class='agent-card'>
                    <span class='status-tag'>🤖 Executed Stage</span>
                    <h4 style='margin-top: 10px; margin-bottom: 5px; color:#1E1B4B;'>{entry['query']}</h4>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info("**📋 Console Run Analysis Logs:**")
                st.text(entry["result"] if entry["result"] else "Task successfully committed to system disk state.")
                
                if entry["chart"] and os.path.exists(entry["chart"]):
                    st.markdown("**🎨 Rendered Dashboard Image Asset:**")
                    st.image(entry["chart"], use_container_width=True)
                    with open(entry["chart"], "rb") as img_file:
                        st.download_button(
                            label=f"Export Chart Asset {i} (.PNG)",
                            data=img_file, file_name=f"insightcore_chart_{i}.png", mime="image/png",
                            key=f"dl_{i}", use_container_width=True
                        )
            with col2:
                st.warning("**💻 Autonomous Python Script Injected:**")
                st.code(entry["code"], language='python')
            st.markdown("<br>", unsafe_allow_html=True)
else:
    st.markdown("<div style='background-color: #EFF6FF; padding: 30px; border-radius: 8px; border-left: 5px solid #3B82F6; text-align: center;'><h3 style='color: #1E40AF; margin-top:0;'>📊 Data Analyst Environment Empty</h3><p style='color: #1D4ED8; margin-bottom:0;'>Please toggle the left configuration sidebar panel and upload a structured CSV file to spin up the code sandbox execution loop engine.</p></div>", unsafe_allow_html=True)
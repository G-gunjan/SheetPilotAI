# import streamlit as st
# import pandas as pd

# from utils.dataframe_utils import load_dataframe
# from components.sidebar import render_sidebar
# from components.dashboard import render_metrics
# from components.command_panel import render_command_panel
# from services.gemini_service import GeminiService
# from services.code_executor import execute_code
# from utils.visualisation import create_visualization

# # ------------------------------------------------
# # PAGE CONFIG
# # ------------------------------------------------
# st.set_page_config(
#     page_title="SheetPilot AI – Voice Macro Builder",
#     page_icon="📊",
#     layout="wide"
# )

# # ------------------------------------------------
# # SESSION STATE
# # ------------------------------------------------
# for key in ["history", "result", "generated_code", "ai_response", "command_input"]:
#     if key not in st.session_state:
#         st.session_state[key] = [] if key == "history" else None

# # ------------------------------------------------
# # HEADER
# # ------------------------------------------------
# st.title("📊 SheetPilot AI")
# st.markdown("### Voice-Activated Excel Macro Builder for Tax Professionals")
# st.markdown("**Upload → Speak / Type → Generate (Pandas or VBA) → Execute → Download**")

# # ------------------------------------------------
# # SIDEBAR
# # ------------------------------------------------
# show_code, show_ai = render_sidebar()

# # ------------------------------------------------
# # FILE UPLOAD
# # ------------------------------------------------
# uploaded_file = st.file_uploader(
#     "Upload your CSV or Excel file",
#     type=["csv", "xlsx", "xls"]
# )

# if uploaded_file is None:
#     st.info("👆 Upload a dataset to start. Then speak or type your command.")
#     st.stop()

# # ------------------------------------------------
# # LOAD DATA
# # ------------------------------------------------
# try:
#     df = load_dataframe(uploaded_file)
# except Exception as e:
#     st.error(f"Unable to load file: {e}")
#     st.stop()

# st.session_state["df"] = df

# # ------------------------------------------------
# # DATASET OVERVIEW
# # ------------------------------------------------
# st.subheader("📈 Dataset Overview")
# render_metrics(df)

# with st.expander("🔎 Preview Dataset", expanded=False):
#     st.dataframe(df.head(100), use_container_width=True)

# # ------------------------------------------------
# # COMMAND PANEL (VOICE + TEXT)
# # ------------------------------------------------
# command, submitted, prefer_vba = render_command_panel()

# # ------------------------------------------------
# # PROCESS COMMAND
# # ------------------------------------------------
# if submitted:
#     if not command or not command.strip():
#         st.warning("Please enter or speak a command.")
#         st.stop()

#     with st.spinner("🧠 SheetPilot is understanding your request..."):
#         try:
#             gemini = GeminiService()
#             ai_response = gemini.generate_command(
#                 command,
#                 df,
#                 prefer_vba=prefer_vba
#             )
#             st.session_state.ai_response = ai_response
#             st.session_state.generated_code = ai_response.get("code")
#         except Exception as e:
#             st.error(f"Gemini error: {e}")
#             st.stop()

# # ------------------------------------------------
# # AI PLAN
# # ------------------------------------------------
# if st.session_state.ai_response:
#     response = st.session_state.ai_response

#     st.subheader("🧠 AI Execution Plan")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown(f"**Intent:** {response.get('intent', 'N/A')}")
#         st.markdown(f"**Operation:** {response.get('operation', 'N/A')}")
#         st.markdown(f"**Code Type:** `{response.get('code_type', 'pandas').upper()}`")

#     with col2:
#         if show_ai:
#             st.info(response.get("explanation", "No explanation available."))

# # ------------------------------------------------
# # GENERATED CODE
# # ------------------------------------------------
# if show_code and st.session_state.generated_code:
#     code_type = st.session_state.ai_response.get("code_type", "pandas")
#     lang = "vb" if code_type == "vba" else "python"

#     with st.expander(f"🐍 Generated {'VBA Macro' if code_type == 'vba' else 'Pandas'} Code", expanded=True):
#         st.code(st.session_state.generated_code, language=lang)

#         if code_type == "vba":
#             st.success("Copy the VBA code above and paste it into the Excel VBA Editor (Alt+F11).")

# # ------------------------------------------------
# # EXECUTION (only for Pandas)
# # ------------------------------------------------
# if st.session_state.generated_code:
#     code_type = st.session_state.ai_response.get("code_type", "pandas")

#     if code_type == "pandas":
#         if st.button("▶️ Execute Generated Code", type="primary"):
#             try:
#                 with st.spinner("Executing operation..."):
#                     result = execute_code(
#                         st.session_state.generated_code,
#                         df
#                     )
#                     st.session_state.result = result
#                     st.session_state.history.append({
#                         "command": command,
#                         "status": "Success"
#                     })
#             except Exception as e:
#                 st.error(f"Execution failed: {e}")
#     else:
#         st.info("VBA macros cannot be executed inside the browser. Copy the code into Excel.")

# # ------------------------------------------------
# # RESULTS
# # ------------------------------------------------
# if st.session_state.result is not None:
#     result = st.session_state.result
#     st.subheader("📊 Execution Result")

#     if isinstance(result, pd.DataFrame):
#         st.dataframe(result, use_container_width=True)

#         csv = result.to_csv(index=False)
#         st.download_button(
#             "📥 Download Result as CSV",
#             csv,
#             "sheetpilot_result.csv",
#             "text/csv"
#         )

#         # Optional chart
#         chart_type = st.session_state.ai_response.get("chart_type")
#         fig = create_visualization(result, chart_type)
#         if fig:
#             st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.write(result)

# # ------------------------------------------------
# # HISTORY
# # ------------------------------------------------
# if st.session_state.history:
#     with st.expander("🕘 Command History"):
#         for item in reversed(st.session_state.history):
#             st.write(f"🎤 {item['command']} — ✅ {item['status']}")


import streamlit as st
import pandas as pd

from utils.dataframe_utils import load_dataframe
from components.sidebar import render_sidebar
from components.dashboard import render_metrics
from components.command_panel import render_command_panel
from services.gemini_service import GeminiService
from services.code_executor import execute_code
from utils.visualisation import create_visualization


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SheetPilot AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

for key in [
    "history",
    "result",
    "generated_code",
    "ai_response",
    "command_input"
]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "history" else None


# ============================================================
# CUSTOM STREAMLIT STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN APP
    ======================================================== */

    .stApp {
        background-color: #f6f8fb;
        color: #111827;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       MAIN CONTENT TEXT
    ======================================================== */

    .main .block-container {
        color: #111827;
    }

    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4 {
        color: #111827 !important;
    }

    .main .block-container p {
        color: #475569;
    }

    .main .block-container label {
        color: #334155 !important;
    }


    /* ========================================================
       TITLE
    ======================================================== */

    .main .block-container h1 {
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .main .block-container h2 {
        font-weight: 750;
    }

    .main .block-container h3 {
        font-weight: 700;
    }


    /* ========================================================
       CAPTIONS
    ======================================================== */

    .main .block-container [data-testid="stCaptionContainer"] {
        color: #64748b !important;
    }


    /* ========================================================
       DIVIDERS
    ======================================================== */

    .main .block-container hr {
        border-color: #e2e8f0;
    }


    /* ========================================================
       BUTTONS
    ======================================================== */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }


    /* ========================================================
       PRIMARY BUTTON
    ======================================================== */

    .stButton > button[kind="primary"] {
        font-weight: 700;
    }


    /* ========================================================
       FILE UPLOADER
    ======================================================== */

    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 10px;
        border: 1px solid #dbe2ea;
    }

    [data-testid="stFileUploader"] label {
        color: #334155 !important;
    }


    /* ========================================================
       METRICS
    ======================================================== */

    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #475569 !important;
    }


    /* ========================================================
       EXPANDERS
    ======================================================== */

    [data-testid="stExpander"] {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        background-color: #ffffff;
    }

    [data-testid="stExpander"] summary {
        color: #111827 !important;
        font-weight: 600;
    }


    /* ========================================================
       INFO / WARNING / SUCCESS BOXES
    ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ========================================================
       DATAFRAME
    ======================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }


    /* ========================================================
       TEXT INPUTS
    ======================================================== */

    textarea,
    input {
        color: #111827 !important;
    }


    /* ========================================================
       WORKFLOW
    ======================================================== */

    .workflow-icon {
        font-size: 30px;
        text-align: center;
        margin-bottom: 4px;
    }

    .workflow-label {
        color: #475569 !important;
        font-size: 13px;
        font-weight: 600;
        text-align: center;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #171923;
    }


    /* ========================================================
       SIDEBAR TEXT
    ======================================================== */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }


    /* ========================================================
       MOBILE
    ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .workflow-icon {
            font-size: 25px;
        }

        .workflow-label {
            font-size: 11px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

show_code, show_ai = render_sidebar()


# ============================================================
# HEADER
# ============================================================

st.title("📊 SheetPilot AI")

st.subheader(
    "Voice-Activated Excel Macro Builder for Tax Professionals"
)

st.caption(
    "Upload → Speak / Type → Generate → Execute → Download"
)

st.divider()


# ============================================================
# WORKFLOW
# ============================================================

st.markdown("### 🔄 How SheetPilot Works")

workflow = st.columns(6)

with workflow[0]:
    st.markdown(
        '<div class="workflow-icon">📁</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="workflow-label">Upload</div>',
        unsafe_allow_html=True
    )

with workflow[1]:
    st.markdown(
        '<div class="workflow-icon">🎤</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="workflow-label">Speak / Type</div>',
        unsafe_allow_html=True
    )

with workflow[2]:
    st.markdown(
        '<div class="workflow-icon">🧠</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="workflow-label">AI Analysis</div>',
        unsafe_allow_html=True
    )

with workflow[3]:
    st.markdown(
        '<div class="workflow-icon">⚙️</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="workflow-label">Generate</div>',
        unsafe_allow_html=True
    )

with workflow[4]:
    st.markdown(
        '<div class="workflow-icon">▶️</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="workflow-label">Execute</div>',
        unsafe_allow_html=True
    )

with workflow[5]:
    st.markdown(
        '<div class="workflow-icon">📥</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="workflow-label">Export</div>',
        unsafe_allow_html=True
    )

st.divider()


# ============================================================
# FILE UPLOAD
# ============================================================

st.markdown("## 📁 Upload Your Dataset")

st.info(
    "Bring your spreadsheet into SheetPilot. "
    "Upload a CSV or Excel file and use natural language "
    "to automate spreadsheet operations."
)

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)


if uploaded_file is None:

    st.warning(
        "👆 Upload a dataset to start. "
        "Then speak or type your command."
    )

    st.stop()


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_dataframe(uploaded_file)

except Exception as e:

    st.error(
        f"Unable to load file: {e}"
    )

    st.stop()


st.session_state["df"] = df


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.markdown("## 📈 Dataset Overview")

render_metrics(df)


with st.expander(
    "🔎 Preview Dataset",
    expanded=False
):

    st.dataframe(
        df.head(100),
        use_container_width=True,
        height=400
    )


# ============================================================
# COMMAND PANEL
# ============================================================

st.markdown("## 🎤 Tell SheetPilot What To Do")

st.info(
    'Describe what you want to do with your spreadsheet '
    'in natural language. Example: '
    '"Filter Q3 revenue and group it by entity."'
)

command, submitted, prefer_vba = render_command_panel()


# ============================================================
# PROCESS COMMAND
# ============================================================

if submitted:

    if not command or not command.strip():

        st.warning(
            "Please enter or speak a command."
        )

        st.stop()


    with st.spinner(
        "🧠 SheetPilot is understanding your request..."
    ):

        try:

            gemini = GeminiService()

            ai_response = gemini.generate_command(
                command,
                df,
                prefer_vba=prefer_vba
            )

            st.session_state.ai_response = ai_response

            st.session_state.generated_code = (
                ai_response.get("code")
            )

        except Exception as e:

            st.error(
                f"Gemini error: {e}"
            )

            st.stop()


# ============================================================
# AI EXECUTION PLAN
# ============================================================

if st.session_state.ai_response:

    response = st.session_state.ai_response

    st.markdown("## 🧠 AI Execution Plan")

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Intent",
            response.get(
                "intent",
                "N/A"
            )
        )


    with col2:

        st.metric(
            "Operation",
            response.get(
                "operation",
                "N/A"
            )
        )


    with col3:

        st.metric(
            "Code Type",
            response.get(
                "code_type",
                "pandas"
            ).upper()
        )


    if show_ai:

        with st.expander(
            "💡 View AI Explanation",
            expanded=True
        ):

            st.write(
                response.get(
                    "explanation",
                    "No explanation available."
                )
            )


# ============================================================
# GENERATED CODE
# ============================================================

if (
    show_code
    and st.session_state.generated_code
):

    code_type = (
        st.session_state.ai_response
        .get(
            "code_type",
            "pandas"
        )
    )


    lang = (
        "vb"
        if code_type == "vba"
        else "python"
    )


    code_title = (
        "VBA Macro"
        if code_type == "vba"
        else "Pandas"
    )


    st.markdown(
        f"## 💻 Generated {code_title} Code"
    )


    with st.expander(
        "View Generated Code",
        expanded=True
    ):

        st.code(
            st.session_state.generated_code,
            language=lang
        )


        if code_type == "vba":

            st.success(
                "Copy the VBA code above and paste it "
                "into the Excel VBA Editor using Alt+F11."
            )


# ============================================================
# EXECUTION
# ============================================================

if st.session_state.generated_code:

    code_type = (
        st.session_state.ai_response
        .get(
            "code_type",
            "pandas"
        )
    )


    st.markdown("## ⚙️ Execute")


    if code_type == "pandas":

        st.info(
            "The generated Pandas code is ready. "
            "Review it above before execution."
        )


        if st.button(
            "▶️ Execute Generated Code",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "⚙️ Executing operation..."
                ):

                    result = execute_code(
                        st.session_state.generated_code,
                        df
                    )


                    st.session_state.result = result


                    st.session_state.history.append(
                        {
                            "command": command,
                            "status": "Success"
                        }
                    )


                st.success(
                    "✅ Operation completed successfully!"
                )


            except Exception as e:

                st.error(
                    f"Execution failed: {e}"
                )


    else:

        st.warning(
            "VBA macros cannot be executed inside "
            "the browser. Copy the generated code "
            "into Excel."
        )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.result is not None:

    result = st.session_state.result

    st.markdown("## 📊 Execution Result")


    if isinstance(
        result,
        pd.DataFrame
    ):

        st.success(
            "✅ Operation completed successfully."
        )


        st.dataframe(
            result,
            use_container_width=True,
            height=450
        )


        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.markdown(
            "### 📥 Export Result"
        )


        csv = result.to_csv(
            index=False
        )


        st.download_button(
            label="📥 Download Result as CSV",
            data=csv,
            file_name="sheetpilot_result.csv",
            mime="text/csv"
        )


        # ====================================================
        # VISUALIZATION
        # ====================================================

        chart_type = (
            st.session_state.ai_response
            .get("chart_type")
        )


        fig = create_visualization(
            result,
            chart_type
        )


        if fig:

            st.markdown(
                "### 📈 Visualization"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


    else:

        st.write(result)


# ============================================================
# HISTORY
# ============================================================

if st.session_state.history:

    st.markdown(
        "## 🕘 Command History"
    )


    with st.expander(
        "View Previous Commands",
        expanded=False
    ):

        for item in reversed(
            st.session_state.history
        ):

            st.write(
                f"🎤 **{item['command']}**"
            )

            st.caption(
                f"Status: {item['status']}"
            )

            st.divider()
import streamlit as st
import pandas as pd

from utils.dataframe_utils import load_dataframe
from components.sidebar import render_sidebar
from components.dashboard import render_metrics
from components.command_panel import render_command_panel
from services.gemini_service import GeminiService
from services.code_executor import execute_code
from utils.visualisation import create_visualization

# PAGE CONFIG

st.set_page_config(
    page_title="SheetPilot AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# SESSION STATE

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "generated_code" not in st.session_state:
    st.session_state.generated_code = None

if "ai_response" not in st.session_state:
    st.session_state.ai_response = None

if "command_input" not in st.session_state:
    st.session_state.command_input = ""

if "voice_command" not in st.session_state:
    st.session_state.voice_command = ""

if "last_command" not in st.session_state:
    st.session_state.last_command = ""


# CUSTOM STREAMLIT STYLING

st.markdown(
    """
    <style>

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .stApp {
        background: #f5f7fb !important;
    }

    .block-container {
        max-width: 1450px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }


    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4 {
        color: #111827 !important;
        opacity: 1 !important;
    }

    [data-testid="stMain"] h1 {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.7px !important;
    }

    [data-testid="stMain"] h2 {
        font-weight: 750 !important;
    }

    [data-testid="stMain"] h3 {
        font-weight: 700 !important;
    }

    [data-testid="stMain"] p {
        color: #334155;
    }

    [data-testid="stMain"] [data-testid="stMarkdownContainer"] {
        color: #111827;
    }

    [data-testid="stMain"]
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMain"]
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMain"]
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMain"]
    [data-testid="stMarkdownContainer"] h4 {
        color: #111827 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #64748b !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #64748b !important;
    }

    [data-testid="stMain"] hr {
        border-color: #dfe5ee !important;
    }



    section[data-testid="stSidebar"] {
        background: #171923 !important;
        border-right: 1px solid #252936 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }



    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: #1e293b !important;
    }



    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 1px solid #dfe5ee !important;
        border-radius: 14px !important;
        padding: 12px !important;
    }

    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] label p {
        color: #111827 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #ffffff !important;
        border: 1px dashed #cbd5e1 !important;
        border-radius: 10px !important;
    }



    [data-testid="stTextArea"] label,
    [data-testid="stTextArea"] label p {
        color: #111827 !important;
        font-weight: 600 !important;
    }

    [data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        caret-color: #111827 !important;

        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;

        min-height: 105px !important;
        padding: 14px 16px !important;

        font-size: 15px !important;
        line-height: 1.5 !important;

        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border: 2px solid #93c5fd !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12) !important;
        outline: none !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        opacity: 1 !important;
    }



    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] label p {
        color: #334155 !important;
    }



    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input {
        background: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }



    [data-testid="stButton"] button {
        min-height: 42px !important;
        border-radius: 10px !important;
        font-weight: 650 !important;
        transition: 0.15s ease !important;
    }



    [data-testid="stButton"] button[kind="secondary"],
    [data-testid="stBaseButton-secondary"] {
        background: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
    }

    [data-testid="stButton"] button[kind="secondary"]:hover,
    [data-testid="stBaseButton-secondary"]:hover {
        background: #f8fafc !important;
        color: #111827 !important;
        border-color: #94a3b8 !important;
    }



    [data-testid="stButton"] button[kind="primary"],
    [data-testid="stBaseButton-primary"] {
        background: #ef2b24 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid #ef2b24 !important;
        font-weight: 750 !important;
        box-shadow: 0 4px 10px rgba(239, 43, 36, 0.18) !important;
    }

    [data-testid="stButton"] button[kind="primary"]:hover,
    [data-testid="stBaseButton-primary"]:hover {
        background: #d91f19 !important;
        color: #ffffff !important;
        border-color: #d91f19 !important;
    }

    [data-testid="stButton"] button p,
    [data-testid="stButton"] button span {
        color: inherit !important;
        -webkit-text-fill-color: inherit !important;
    }



    [data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05) !important;
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


    /* ---------- EXPANDERS ---------- */

    [data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary span {
        color: #111827 !important;
        font-weight: 650 !important;
    }



    [data-testid="stDataFrame"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }



    [data-testid="stCodeBlock"] {
        border-radius: 12px !important;
    }



    [data-testid="stDownloadButton"] button {
        background: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-weight: 650 !important;
    }

    [data-testid="stDownloadButton"] button:hover {
        background: #f8fafc !important;
        border-color: #94a3b8 !important;
    }



    .workflow-icon {
        font-size: 30px;
        text-align: center;
        margin-bottom: 5px;
    }

    .workflow-label {
        color: #475569 !important;
        font-size: 13px;
        font-weight: 650;
        text-align: center;
    }



    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
        }

        [data-testid="stMain"] h1 {
            font-size: 1.8rem !important;
        }

        .workflow-icon {
            font-size: 24px;
        }

        .workflow-label {
            font-size: 10px;
        }

        [data-testid="stTextArea"] textarea {
            min-height: 90px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)




show_code, show_ai = render_sidebar()




st.title("📊 SheetPilot AI")

st.subheader(
    "Voice-Activated Excel Macro Builder for Tax Professionals"
)

st.caption(
    "Upload → Speak / Type → AI Analysis → Generate → Execute → Export"
)

st.divider()


st.markdown("### 🔄 How SheetPilot Works")

workflow = st.columns(6)

workflow_steps = [
    ("📁", "Upload"),
    ("🎤", "Speak / Type"),
    ("🧠", "AI Analysis"),
    ("⚙️", "Generate"),
    ("▶️", "Execute"),
    ("📥", "Export")
]

for col, (icon, label) in zip(workflow, workflow_steps):

    with col:

        st.markdown(
            f'<div class="workflow-icon">{icon}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="workflow-label">{label}</div>',
            unsafe_allow_html=True
        )

st.divider()




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


try:

    df = load_dataframe(uploaded_file)

except Exception as e:

    st.error(
        f"Unable to load file: {e}"
    )

    st.stop()


# Store dataframe

st.session_state["df"] = df


st.markdown("## 📈 Dataset Overview")

try:

    render_metrics(df)

except Exception as e:

    st.warning(
        f"Unable to render dataset metrics: {e}"
    )


with st.expander(
    "🔎 Preview Dataset",
    expanded=False
):

    st.dataframe(
        df.head(100),
        use_container_width=True,
        height=400
    )



st.markdown("## 🎤 Tell SheetPilot What To Do")

st.info(
    'Describe what you want to do with your spreadsheet '
    'in natural language. Example: '
    '"Filter Q3 revenue and group it by entity."'
)

command, submitted, prefer_vba = render_command_panel()


if submitted:

    if not command or not command.strip():

        st.warning(
            "⚠️ Please enter or speak a command."
        )

    else:

        # Save command for history
        st.session_state.last_command = command

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

                # Validate AI response

                if not isinstance(ai_response, dict):

                    raise ValueError(
                        "Gemini returned an invalid response."
                    )

                st.session_state.ai_response = ai_response

                st.session_state.generated_code = (
                    ai_response.get("code")
                )

                # Clear previous execution result
                st.session_state.result = None

                st.success(
                    "✅ AI command generated successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Gemini error: {e}"
                )


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


if (
    show_code
    and st.session_state.generated_code
    and st.session_state.ai_response
):

    code_type = (
        st.session_state.ai_response.get(
            "code_type",
            "pandas"
        )
    )

    lang = (
        "vb"
        if code_type.lower() == "vba"
        else "python"
    )

    code_title = (
        "VBA Macro"
        if code_type.lower() == "vba"
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

        if code_type.lower() == "vba":

            st.success(
                "📋 Copy the VBA code above and paste it "
                "into the Excel VBA Editor using Alt+F11."
            )


if (
    st.session_state.generated_code
    and st.session_state.ai_response
):

    code_type = (
        st.session_state.ai_response.get(
            "code_type",
            "pandas"
        )
    )

    st.markdown("## ⚙️ Execute")


    if code_type.lower() == "pandas":

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

                # Validate result

                if result is None:

                    raise ValueError(
                        "Generated code did not return a result."
                    )

                st.session_state.result = result

                # Add to history

                st.session_state.history.append(
                    {
                        "command": (
                            st.session_state.last_command
                            or st.session_state.command_input
                        ),
                        "status": "Success"
                    }
                )

                st.success(
                    "✅ Operation completed successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Execution failed: {e}"
                )

    else:

        st.warning(
            "⚠️ VBA macros cannot be executed inside "
            "the browser. Copy the generated code "
            "into Excel."
        )



if st.session_state.result is not None:

    result = st.session_state.result

    st.markdown("## 📊 Execution Result")

 

    if isinstance(result, pd.DataFrame):

        st.success(
            "✅ Operation completed successfully."
        )

        st.dataframe(
            result,
            use_container_width=True,
            height=450
        )

    

        st.markdown("### 📥 Export Result")

        csv_data = result.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Result as CSV",
            data=csv_data,
            file_name="sheetpilot_result.csv",
            mime="text/csv",
            use_container_width=False
        )


        if st.session_state.ai_response:

            chart_type = (
                st.session_state.ai_response.get(
                    "chart_type"
                )
            )

            try:

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

            except Exception as e:

                st.warning(
                    f"Unable to create visualization: {e}"
                )


    else:

        st.write(result)



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
                f"🎤 **{item.get('command', 'Unknown command')}**"
            )

            st.caption(
                f"Status: {item.get('status', 'Unknown')}"
            )

            st.divider()
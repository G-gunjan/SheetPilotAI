# import streamlit as st


# def render_sidebar():

#     with st.sidebar:

#         st.title("⚙️ SheetPilot")

#         st.markdown("---")

#         st.subheader("Settings")

#         show_code = st.checkbox(
#             "Show generated code",
#             value=True
#         )

#         show_ai = st.checkbox(
#             "Show AI explanation",
#             value=True
#         )

#         st.markdown("---")

#         st.caption(
#             "AI-powered spreadsheet automation"
#         )

#     return show_code, show_ai



import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ SheetPilot AI")
        st.caption("Voice-Activated Excel Macro Builder")
        st.markdown("---")

        st.subheader("Display Options")
        show_code = st.checkbox("Show generated code", value=True)
        show_ai = st.checkbox("Show AI explanation", value=True)

        st.markdown("---")
        st.subheader("Tax Pro Tips")
        st.markdown("""
        - Speak naturally: “Filter Q3 revenue”
        - Ask for VBA: “Make a macro that…”
        - Common tax ops: filter by period, group by entity, sum taxable income, highlight overdue
        """)
        st.markdown("---")
        st.caption("Powered by Gemini • Safe code execution")

    return show_code, show_ai
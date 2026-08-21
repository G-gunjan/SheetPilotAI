# import streamlit as st


# def render_command_panel():

#     st.subheader("🎤 Ask SheetPilot")

#     with st.form("command_form"):

#         command = st.text_area(
#             "Tell me what you want to do with your dataset:",
#             placeholder=(
#                 "Example: Show the top 10 customers "
#                 "by profit in Maharashtra."
#             ),
#             height=100
#         )

#         submitted = st.form_submit_button(
#             "🚀 Run Command"
#         )

#     return command, submitted


import streamlit as st
import speech_recognition as sr

def render_command_panel():
    st.subheader("🎤 Ask SheetPilot (Voice or Text)")

    # Voice input section
    col1, col2 = st.columns([3, 1])

    with col1:
        command = st.text_area(
            "Type or speak your command:",
            placeholder=(
                "Examples:\n"
                "• Filter Q3 revenue for California\n"
                "• Show top 10 clients by taxable income\n"
                "• Create VBA macro to highlight overdue invoices\n"
                "• Group by state and sum sales tax"
            ),
            height=120,
            key="command_input"
        )

    with col2:
        st.write("")  # spacing
        st.write("")
        if st.button("🎙️ Speak Command", use_container_width=True, type="secondary"):
            with st.spinner("Listening... Speak now"):
                try:
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        audio = r.listen(source, timeout=5, phrase_time_limit=15)

                    text = r.recognize_google(audio)
                    st.session_state.command_input = text
                    st.success(f"Heard: **{text}**")
                    st.rerun()
                except sr.WaitTimeoutError:
                    st.warning("No speech detected. Try again.")
                except sr.UnknownValueError:
                    st.warning("Could not understand audio. Please try again.")
                except Exception as e:
                    st.error(f"Voice error: {e}")

    # Preference for VBA
    prefer_vba = st.checkbox(
        "Prefer Excel VBA macro (instead of Pandas)",
        value=False,
        help="When checked, SheetPilot will generate ready-to-paste VBA code."
    )

    submitted = st.button("🚀 Run Command", type="primary", use_container_width=True)

    return command, submitted, prefer_vba
# import streamlit as st
# import speech_recognition as sr

# def render_command_panel():
#     st.subheader("🎤 Ask SheetPilot (Voice or Text)")

#     # Voice input section
#     col1, col2 = st.columns([3, 1])

#     with col1:
#         command = st.text_area(
#             "Type or speak your command:",
#             placeholder=(
#                 "Examples:\n"
#                 "• Filter Q3 revenue for California\n"
#                 "• Show top 10 clients by taxable income\n"
#                 "• Create VBA macro to highlight overdue invoices\n"
#                 "• Group by state and sum sales tax"
#             ),
#             height=120,
#             key="command_input"
#         )

#     with col2:
#         st.write("")  # spacing
#         st.write("")
#         if st.button("🎙️ Speak Command", use_container_width=True, type="secondary"):
#             with st.spinner("Listening... Speak now"):
#                 try:
#                     r = sr.Recognizer()
#                     with sr.Microphone() as source:
#                         r.adjust_for_ambient_noise(source, duration=0.5)
#                         audio = r.listen(source, timeout=5, phrase_time_limit=15)

#                     text = r.recognize_google(audio)
#                     st.session_state.command_input = text
#                     st.success(f"Heard: **{text}**")
#                     st.rerun()
#                 except sr.WaitTimeoutError:
#                     st.warning("No speech detected. Try again.")
#                 except sr.UnknownValueError:
#                     st.warning("Could not understand audio. Please try again.")
#                 except Exception as e:
#                     st.error(f"Voice error: {e}")

#     # Preference for VBA
#     prefer_vba = st.checkbox(
#         "Prefer Excel VBA macro (instead of Pandas)",
#         value=False,
#         help="When checked, SheetPilot will generate ready-to-paste VBA code."
#     )

#     submitted = st.button("🚀 Run Command", type="primary", use_container_width=True)

#     return command, submitted, prefer_vba



import streamlit as st
import speech_recognition as sr


def render_command_panel():

    st.subheader("🎤 Ask SheetPilot (Voice or Text)")

    # =========================================================
    # SESSION STATE
    # =========================================================

    if "command_input" not in st.session_state:
        st.session_state.command_input = ""

    if "voice_command" not in st.session_state:
        st.session_state.voice_command = ""

    # =========================================================
    # IMPORTANT:
    # Transfer voice text BEFORE creating the text_area widget.
    # =========================================================

    if st.session_state.voice_command:

        st.session_state.command_input = (
            st.session_state.voice_command
        )

        st.session_state.voice_command = ""

    # =========================================================
    # COMMAND INPUT
    # =========================================================

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

    # =========================================================
    # VOICE INPUT
    # =========================================================

    with col2:

        st.write("")
        st.write("")
        st.write("")

        if st.button(
            "🎙️ Speak Command",
            use_container_width=True,
            type="secondary"
        ):

            with st.spinner("🎙️ Listening... Speak now"):

                try:

                    recognizer = sr.Recognizer()

                    with sr.Microphone() as source:

                        recognizer.adjust_for_ambient_noise(
                            source,
                            duration=0.5
                        )

                        audio = recognizer.listen(
                            source,
                            timeout=5,
                            phrase_time_limit=15
                        )

                    text = recognizer.recognize_google(audio)

                    # DO NOT modify command_input here.
                    # Store voice result separately.

                    st.session_state.voice_command = text

                    st.rerun()

                except sr.WaitTimeoutError:

                    st.warning(
                        "⏱️ No speech detected. Please try again."
                    )

                except sr.UnknownValueError:

                    st.warning(
                        "❌ Could not understand your speech. "
                        "Please try again."
                    )

                except sr.RequestError as e:

                    st.error(
                        f"❌ Speech recognition service error: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"❌ Voice error: {e}"
                    )

    # =========================================================
    # VBA PREFERENCE
    # =========================================================

    prefer_vba = st.checkbox(
        "Prefer Excel VBA macro (instead of Pandas)",
        value=False,
        help=(
            "When checked, SheetPilot will generate "
            "ready-to-paste VBA code."
        )
    )

    # =========================================================
    # RUN COMMAND
    # =========================================================

    submitted = st.button(
        "🚀 Run Command",
        type="primary",
        use_container_width=True
    )

    return command, submitted, prefer_vba
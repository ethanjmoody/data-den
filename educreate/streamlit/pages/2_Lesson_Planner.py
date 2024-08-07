# Import modules and packages
import locale
import streamlit as st

from audio_summary import extract, setup_pipeline
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

locale.getpreferredencoding = lambda: "UTF-8"

st.set_page_config(page_title = "Lesson Planner")

st.logo('EduCreate.png')

st.sidebar.success("""
    1. (Optional) Change the default lesson plan creation instruction. **Don't forget to hit Enter to apply!**
    2. Select the type of video content to analyze (either YouTube or other).
    3. Provide a URL link to the video. 
    4. Click button to create lesson plan. 
    5. Click button to download generated lesson plan.
""")

user_prompt = """
Please summarise the key points from the lesson and in a useful order for students who missed this live lesson.
Please also suggest some questions (and answers) for follow up work by the students.
"""

def main():
    ctx = get_script_run_ctx()

    setup_pipeline(ctx.session_id)

    text = st.text_area('1️⃣ Enter lesson plan creation instruction. The default option is shown in grey.', 
    placeholder =  "Please summarise the key points from the lesson and in a useful order for students who missed this live lesson. Please also suggest some questions (and answers) for follow up work by the students.",
    value =  "Please summarise the key points from the lesson and in a useful order for students who missed this live lesson. Please also suggest some questions (and answers) for follow up work by the students."
    )

    video_type = st.radio(
        "2️⃣ Set video type",
        key="video_type",
        options=["YouTube", "Other"]
    )

    url = st.text_input('3️⃣ URL link to the video (must be accessible online)')

    col1, col2 = st.columns([3,7])

    if col1.button("4️⃣ Generate Lesson Plan"):
        transcription = extract(video_type, url, text)
        st.session_state['transcription'] = transcription
        st.write(transcription)
    
    col2.download_button(
        label = "5️⃣ Download Lesson Plan", 
        data = st.session_state['transcription'],
        file_name = "Lesson plan.txt",
        mime="text")

    st.write(st.session_state['transcription'])
if __name__ == "__main__":
    main()
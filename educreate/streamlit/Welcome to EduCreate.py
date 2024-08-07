import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to EduCreate! 👋")

st.logo('EduCreate.png')

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    ### Empowering the Content Creator within Every Teacher
    EduCreate is an innovative, open-source app framework designed to help educators create personalized content using cutting-edge Generative AI technologies. With EduCreate, you can transform traditional educational materials in just three simple steps!

    ### Why Choose EduCreate?
    - **Free and Secure**: Although it leverages some commercial APIs, the EduCreate pipeline is free to use! No user provided data are stored, ensuring your privacy and security.
    - **Focused on High School History**: Version 1.0 is tailored specifically for high school history classes, offering unique features to enhance your teaching experience.
    
    ### Features of Version 1.0
    1. Comic Generator: Transform Textbook Chapters into Comic Stories
        - Bring history to life by converting traditional chapters or pages from History textbooks into engaging comic stories.
        - Capture students' interest and make learning more fun and interactive.
    2. Lesson Planner: Convert Videos into Lesson Plans
        - Turn any video recording or YouTube video into a comprehensive follow-up lesson plan.
        - Save time on lesson preparation while ensuring your students get the most out of multimedia resources.

    ### Want to learn more?
    - Jump into our [documentation](https://github.com/ykinakin/educreate)
    - Want to learn more or have a suggestion for improvement? [Sign up form](https://docs.google.com/forms/d/1NQgTsHV5vNsJ1Z_SzNdN9PKNgf45ucqghI24F2vj_2c/edit?ts=669f4158)
"""
)

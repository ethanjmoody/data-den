import easyocr
import os
import pymupdf
import streamlit as st


from comic_poc import style_list, setup_pipeline, create_story_prompt, create_image_prompts, create_images, create_comic_strip, initialize_session
from keys import huggingface_token, anthropic_token, openai_token
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
from io import BytesIO
from PIL import Image

st.set_page_config(page_title = "Comic Generator")

st.logo('EduCreate.png')

st.sidebar.success("""
    1. Type in the main objective for your lesson. **Don't forget to hit Enter to apply!**
    2. Select a comic style.
    3. (Optional) Upload a file that is aligned to your lesson objective to provide additional specific information to the language model.
    4. Select the large language model.
    5. Click the 'Generate Text' button to generate a written summary of the lesson objective.
    6. Click the 'Generate Comic' button to generate a comic based on the lesson objective. 
    7. Select the output type for the text summary.
    8. Click the "Download Text" button to save a local copy of the text summary. 
    9. Click the "Download Comic" button to save a local copy of the comic. 
    10. If you'd like to change the style of comic generated for a given lesson objective, return to steps 4 and 5 and regenerate the text before clicking again on generate comic.
""")

def main():
    
    ctx = get_script_run_ctx()

    initialize_session(ctx.session_id, anthropic_token, openai_token)

    pipe, rag_retriever = setup_pipeline(huggingface_token)

    lesson_objective = st.text_area(
        "1️⃣ Main lesson objective",
        "",
        key="lesson_objective",
        help="""When prompting, try to be as specific as possible. For example, instead of  
        ***Explain the Berlin Wall***   
        try something like  
        ***Explain the Berlin Wall from an East German perspective with an emphasis on the most significant individuals and their role in how the wall was constructed***  
        The model has additional knowledge of the following topics and will therefore be able to provide a more detailed answer to queries on:  
        Ancient and Medieval History (European Focus)  
        US History  
        20th Century History  
        """,
    )

    # Create style prompt
    comic_style =st.radio(
        "2️⃣ Set comic style",
        key="comic_style",
        options=["Japanese Anime", "Disney Pixar", "Golden Age", "Toon", "Simpsons", "Stick Figure"],
        horizontal = True
    )

    uploaded_file = st.file_uploader('3️⃣ (Optional) Upload a file', type = ['pdf', 'txt', 'jpg'])

    negative_prompt = style_list.get(comic_style).get('negative_prompt')
    style_prompt = style_list.get(comic_style).get('prompt')

    col3, col4 = st.columns(2)
    col5, col6, col7, col8 = st.columns(4)

    model_type = col3.radio(
        "4️⃣ Select model type",
        key="model type",
        options=["Anthropic", "OpenAI"],
        horizontal = True,
        help=""" Current model options are  
        Anthropic Claude 3.5  
        OpenAI GPT-4o"""
    )

    if uploaded_file is not None:
        text = ""
        suffix = uploaded_file.name[-3:]
        if suffix == 'pdf':
            doc = pymupdf.open(stream=uploaded_file.read(), filetype='pdf')
            for page in doc:
                text += page.get_text()
        elif suffix == 'jpg' or suffix == 'jpeg':
            image_bytes = uploaded_file.read()
            image_reader = easyocr.Reader(["en"])
            image_results = image_reader.readtext(image_bytes)
            text = " ".join(result[1] for result in image_results)
        elif suffix == 'txt':
            text = uploaded_file.read()

    prompt_button = col5.button("5️⃣ Generate Text", key = 'pbutton')
    
    if prompt_button:
        if len(lesson_objective) <= 5:
            st.error('Please enter a lesson objective into the text box!', icon="🚨")
        else:
            summ_response = create_story_prompt(rag_retriever, st.session_state['token_dict'][model_type], lesson_objective, st.session_state.text, model_type)
            captions, combined_prompt = create_image_prompts(st.session_state['token_dict'][model_type], summ_response, style_prompt, model_type)
            st.session_state.summ_response = summ_response
            st.session_state.captions = captions
            st.session_state.combined_prompt = combined_prompt

    if col6.button("6️⃣ Generate Comic"):
        if len(st.session_state['captions']) <= 5:
            st.error('Please first generate text!', icon="🚨")
        else:
            captions = st.session_state.captions
            combined_prompt = st.session_state.combined_prompt

            images = create_images(combined_prompt, pipe, negative_prompt)

            font_path = os.getcwd() + '/ComicNeue-BoldItalic.ttf'
            ec_path = os.getcwd() + "/EduCreate.png"
            ec_logo = Image.open(ec_path)
            if len(images) % 2 == 1:
                images.append(ec_logo)
                captions.append("")

            panels_horizontal = len(images)//2
            panels_vertical = 2
            comic_strip = create_comic_strip(images, captions, image_width = 1024,  image_height = 1024, panels_horizontal=panels_horizontal, panels_vertical=panels_vertical, border_size=10, text_height=150, font_path=font_path, font_size=30)
            st.session_state.comic_strip = comic_strip
            buf = BytesIO()
            st.session_state['comic_strip'].save(buf, format="png")
            st.session_state['comic_output'] = buf.getvalue()


    text_type = col4.radio(
        "7️⃣ Select text output",
        key="text download",
        options=["txt", "doc"],
        horizontal = True
    )

    col7.download_button(
        label = "8️⃣ Download Text", 
        data = st.session_state['summ_response'],
        file_name = "Summary document." + text_type,
        mime=text_type)

    col8.download_button(
        label = "9️⃣ Download Comic", 
        data = st.session_state['comic_output'],
        file_name = "Historical_comic.png",
        mime="image/png")
    
    st.write(st.session_state.comic_strip)
    st.write(st.session_state.summ_response)

if __name__ == "__main__":
    main()

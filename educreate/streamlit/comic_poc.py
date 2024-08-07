import json
import math
import os
import pickle

import textwrap
import streamlit as st
import torch

from anthropic import Anthropic
from diffusers import StableDiffusion3Pipeline
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from transformers import T5EncoderModel, BitsAndBytesConfig

style_list = {"Japanese Anime": {
        "prompt": "coloured anime artwork created by a Japanese anime studio, (Anime Style:1.3), (Manga Style:1.3), highly emotional, vibrant colors, best quality, high resolution",
        "negative_prompt": "speech bubbles, low resolution, bad anatomy, bad hands, text, errors, missing fingers, extra digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, username, blurry"}
    ,
    "Disney Pixar": {
        "prompt": "vibrant Disney Pixar 3D style illustration, (Disney Pixar Style:1.3), motivational, vivid colors, sense of wonder, best quality, high resolution",
        "negative_prompt": "speech bubbles, low resolution, bad anatomy, bad hands, text, bad eyes, bad arms, bad legs, errors, missing fingers, extra digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry, grayscale, noisy, sloppy, messy, grainy, highly detailed, ultra-textured, photo"}
    ,
    "Golden Age": {
        "prompt": "coloured comic style with expressive characters and detailed backgrounds, (Comic Style:1.3), vibrant colors, dynamic poses, best quality, high resolution",
        "negative_prompt": "speech bubbles, photograph, deformed, glitch, noisy, realistic, stock photo, low resolution, bad anatomy, bad proportions, bad hands, text, errors, missing fingers, extra digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, username, blurry"}
    ,
    "Toon": {
        "prompt": "vibrant and colorful toon-style illustration, (Toon Style:1.3), exaggerated features, playful characters, simplified shapes, bold outlines, high quality, high resolution",
        "negative_prompt": "low resolution, bad anatomy, bad hands, text, errors, missing fingers, extra digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, username, blurry, realistic details, dark colors, serious expressions"}
    ,
    "Simpsons": {
        "prompt": "coloured illustration in the style of The Simpsons, characterized by exaggerated features, vibrant colors, and a cartoonish aesthetic. Characters with large eyes, overbites, and a humorous expression.",
        "negative_prompt": "realistic, highly detailed, photograph, 3D rendering, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, grayscale, noisy, sloppy, messy, grainy"}
     ,
     "Stick Figure": {
        "prompt": "stick figures, simplified, black and white, cartoonish aesthetic, xkcd, line drawing.",
        "negative_prompt": "realistic, photo, highly detailed, photograph, 3D rendering, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, blurry, grayscale, noisy, grainy"}
    }

@st.cache_resource
def setup_pipeline(huggingface_token):
    torch.cuda.set_device(1)
    quantization_config = BitsAndBytesConfig(load_in_8bit=True)
    model_id = "stabilityai/stable-diffusion-3-medium-diffusers"

    #Check to see if the RAG model has yet been run and pickled. 
    if os.path.exists('./retriever.pkl'):
        pass
    else:
        import rag_poc

    with open("retriever.pkl",'rb') as input_file:
        rag_retriever = pickle.load(input_file)

    text_encoder = T5EncoderModel.from_pretrained(model_id,
                                                subfolder="text_encoder_3",
                                                quantization_config=quantization_config,
                                                cache_dir = './hub',
                                                token = huggingface_token
                                                )

    pipe = StableDiffusion3Pipeline.from_pretrained(model_id,
                                                    text_encoder_3=text_encoder,
                                                    device_map="balanced",
                                                    torch_dtype=torch.float16,
                                                    cache_dir = './hub',
                                                    token = huggingface_token
                                                )

    torch.cuda.empty_cache()

    return pipe, rag_retriever

@st.cache_resource
def initialize_session(user_session_id, anthropic_token, openai_token):
    st.session_state['comic_strip'] = ""
    st.session_state['captions'] = ""
    st.session_state['comic_output'] = ""
    st.session_state['text'] = ""
    st.session_state['summ_response'] = ""
    st.session_state['token_dict'] = dict(zip(["Anthropic","OpenAI"], [anthropic_token, openai_token]))

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_story_prompt(retriever, token, user_prompt, user_input, model_type):
    summ_rag_template = """You are an expert in a broad range of History topics.
        History teachers will be asking questions or provide instructions about a specific topic to help prepare classroom materials.
        Provide detailed response for the question or instructions catering to high school students.

        Please respond to the question or instruction below based on the context information provided.
        JUST ANSWER the question or instruction. DO NOT ADD replies such as 'Of Course!', 'Certainly' etc.
        You may add factual information from your corpus of knowledge BUT ensure the additional information is factual.
        \n\nHere are the topics and context:\n{context} """ + user_input + """\n\nHere is a question: \n{question}."""
    
    summ_rag_prompt = ChatPromptTemplate.from_template(summ_rag_template)

    output_parser = StrOutputParser()

    if model_type == 'Anthropic':
        chat_model = ChatAnthropic(anthropic_api_key=token,
                                model="claude-3-5-sonnet-20240620",
                                temperature = 0.3)

        rag_chain = (
            {"context": retriever | format_docs,
            "question": RunnablePassthrough()}
            | summ_rag_prompt
            | chat_model
            | output_parser
            )

        client = Anthropic(api_key=token)

        user_prompt_improved = client.messages.create(
        max_tokens=2048,
        model="claude-3-5-sonnet-20240620",
        system = "Improve the question or instruction prompt provided for the Retrieval-Augmented Generation model. The improved prompt should NOT EXCEED 50 words.",
        messages=[
            {"role": "user", "content": user_prompt},
            {"role":"assistant", "content":"A better version of the question is:"}
        ]
        )
        output = user_prompt_improved.content[0].text    

    elif model_type == 'OpenAI':
        chat_model = ChatOpenAI(api_key=token,
                               model="gpt-4o-mini",
                               max_tokens=512,
                               timeout=None,
                               temperature=0.3,
                               max_retries=2)

        rag_chain = (
            {"context": retriever | format_docs,
            "question": RunnablePassthrough()}
            | summ_rag_prompt
            | chat_model
            | output_parser
            )

        client = OpenAI(api_key = token)

        user_prompt_improved = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
            {"role": "system", "content": "Improve the question or instruction prompt provided for the Retrieval-Augmented Generation model. The improved prompt should NOT EXCEED 50 words. Just provide the answer."},
            {"role": "user", "content": user_prompt}])

        output = user_prompt_improved.choices[0].message.content

    summ_response = rag_chain.invoke(output)
    return summ_response

def create_image_prompts(token, summ_response, style_prompt, model_type):
    system_content = """
    You are a prolific comic script writer and a computer vision guru.
    You will be given a historical account and you need to turn that into a comic script that will be used to prompt image generation to create the comic.

    READ the instructions LINE BY LINE below.

    Your response will have 4 components as follows:
    1. "character": Provide description of the character including clothing and facial features, or NAME if it is a well known character. DO NOT EXCEED 7 WORDS.
    2. "context": Provide description of the scene and historical setting. DO NOT EXCEED 5 WORDS.
    3. "script": Provide a LIST that sets out each script sequence IN DETAIL. USE {character} ONLY when referring to the "character" in the script.
    4. "caption": Provide a LIST of historical DETAILED descriptions for each script sequence. The number of captions should EQUAL the number of script sequence. Ensure the length of the captions are sufficiently long to be meaningful. DO NOT USE {character} as reference in the captions.
    5. "title": Provide a title for the script.

    Your response should be in the following DICTIONARY format:
    {"character": '...', "context": '...', "script": ['...','...',...], "caption": ['...','...',...], "title": '...'}

    Here is an example of what your response should look like:
    {"character": 'a middle aged Wall Street trader wearing a blue suit with slicked hair called John', "context": 'the year is 1929 with a scene in New York Stock Exchange', "script": ['{character} frantically shouting orders on the crowded trading floor, surrounded by panicked traders and falling stock prices', '{character} staring at the stock ticker in disbelief as the numbers plummet rapidly, signaling the crash.'], "caption": ['1. The New York Stock Exchange is a frenzy of activity as traders like John try to salvage their investments amidst the chaos of falling stock prices.', '2. Numbers on the stock ticker flash red as John watches in shock and horror at the speed of the market crash unfolding before his eyes.'], "title": 'Black Tuesday'}
    """

    user_content = """
    The year for 1962 at the height of the Cold War. The world was at its closest to a nuclear war that would be disasterous for all countries.
    President John F Kennedy just received news from his advisers that missiles sites have been discovered in Cuba. He needs to decide the next course of actions.
    He is presented with several options and he needs to consider each one carefully. Finally, he decided Blockade is the best option and it turns out to be a great decision.
    """

    assistant_content = """
    {"character": "President John F Kennedy, a young 45 year old gentlemen, wearing a smart dark blue suit, with black hair, blue eyes and slick hair.",
    "context": "Time period is 1960s in the United States of America.",
    "script": ["{character} is sitting in the Oval office with his assistant standing next to him briefing him on a report.",
            "{character} is holding a meeting with his advisers on a long table in a meeting room. The advisers are sat opposite each other on the long table.",
            "{character} points to a paper report on the table as he addresses his advisers. The paper report contains information about missile sites in Cuba.",
            "{character} watched his advisers arguing angrily with each other about what {character} should do.",
            "{character} sits in a leather sofa in the Oval office thinking hard about the next steps. There are different options swirling in his mind.",
            "{character} makes an announcement on a Presidential podium to a room full of reporters that there will be a Cuban blockade."],
    "caption": ["1. President John F Kennedy receives a report from his adviser that missile sites have been found in Cuba. The year was 1962.",
                "2. He called for a meeting with advisers to discuss what to do next. On one side he has the 'Doves' and on the other he has the 'Hawks'.",
                "3. President John F Kennedy: Gentlemen! The hour is upon us. Here is the report I received about Fidel Castro and the agreement with the Soviet Union to place nuclear missiles within attacking distance of the United States.",
                "4. The advisers argued about what should be done. Seven different options were laid on the table.",
                "5. President John F Kennedy thought to himself about what he should do next. The next move will change the course of history.",
                "6. After much deliberation, he set Robert Kennedy to strike a deal with Khrushchev. In the mean time, he announced to the world that a blockade will be introduced."],
    "title": "JFK and the Cuban Missile Crisis"}
    """

    if model_type == 'Anthropic':
        client = Anthropic(api_key=token)
        image_response = client.messages.create(
            max_tokens=2048,
            model="claude-3-5-sonnet-20240620",
            system = system_content,
            messages=[
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content},
                {"role": "user", "content": summ_response}
            ]
        )
        rag_results_final = json.loads(image_response.content[0].text)

    elif model_type == 'OpenAI':
        client = OpenAI(api_key = token)
        image_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content},
                {"role": "user", "content": summ_response}
            ]
        )
        rag_results_final = json.loads(image_response.choices[0].message.content)

    character_prompt = rag_results_final["character"]
    context_prompt = rag_results_final["context"]
    story_prompt = rag_results_final["script"]
    captions = rag_results_final["caption"]

    combined_prompt = []

    for story in story_prompt:
        comb_prom = context_prompt + "; " + story.replace("{character}", character_prompt) + "; " + style_prompt
        combined_prompt.append(comb_prom)

    return captions, combined_prompt

# Generate images
def create_images(combined_prompt, pipe, negative_prompt):
    seed = 1924
    generator = torch.Generator("cuda").manual_seed(seed)
    comic_images = []

    progress_bar = st.progress(0, "Generating Images")
    total_len = len(combined_prompt)
    i = 0

    for prompt in combined_prompt:
        image = pipe(prompt=prompt,
                    negative_prompt_3=negative_prompt,
                    num_inference_steps=50,
                    height=1024,
                    width=1024,
                    guidance_scale=7.0,
                    generator=generator).images[0]
        comic_images.append(image)
        i+=1
        progress_bar.progress(i/total_len, "Generating Images")
        torch.cuda.empty_cache()

    return comic_images

def create_comic_strip(images, texts, image_width, image_height, panels_horizontal, panels_vertical, border_size=10, text_height=150, font_path=None, font_size=40, max_caption = 45):
    """
    Organize images into a comic strip with borders and text boxes.

    Arguments:
    images: List of image file paths
    texts: List of text descriptions for each panel
    output_path: Path to save the final comic strip
    image_width: Width of each image
    image_height: Height of each image
    panels_horizontal: Number of panels placed horizontally
    panels_vertical: Number of panels placed vertically
    border_size: Size of the border around each panel
    text_height: Height of the text box at the bottom of each panel
    font_path: Path to the font file for the text
    font_size: Font size for the text
    max_captions: Maximum number of words in a caption
    """
    # Ensure the number of images matches the number of panels
    num_panels = panels_horizontal * panels_vertical
    if len(images) != num_panels:
        raise ValueError(f"The number of images ({len(images)}) does not match the total number of panels ({num_panels})")

    # Ensure the number of texts matches the number of panels
    if len(texts) != num_panels:
        raise ValueError(f"The number of texts ({len(texts)}) does not match the total number of panels ({num_panels})")

    # Check highest number of words in the captions
    caption_word_counts = []
    for caption in texts:
      caption_words = caption.split()
      word_caption_count = len(caption_words)
      caption_word_counts.append(word_caption_count)

    max_caption_word = max(caption_word_counts)

    # Determine text box size
    mult_standard_text_box = math.ceil(2 * max_caption_word / max_caption) / 2
    text_height = math.ceil(mult_standard_text_box * text_height)

    # Calculate total dimensions of the comic strip
    total_width = (image_width + 2 * border_size) * panels_horizontal
    total_height = (image_height + 2 * border_size + text_height) * panels_vertical

    # Create a new image with the total dimensions
    new_image = Image.new('RGB', (total_width, total_height), 'white')

    # Load the font
    font = ImageFont.truetype(font_path, size=font_size) if font_path else ImageFont.load_default()

    # Paste images into the new image
    for i, (image, text) in enumerate(zip(images, texts)):
        image = image.resize((image_width, image_height))

        # Create a panel with a border
        panel = Image.new('RGB', (image_width + 2 * border_size, image_height + 2 * border_size + text_height), 'white')
        panel.paste(image, (border_size, border_size))

        # Draw the text box
        draw = ImageDraw.Draw(panel)
        text_position = (border_size, image_height + 2 * border_size)
        draw.rectangle([text_position, (panel.width - border_size, panel.height - border_size)], fill="white")

        # Wrap the text to fit within the text box
        wrapped_text = textwrap.fill(text, width=(image_width // font_size * 2))

        # Add the text to the text box
        draw.text((text_position[0] + 10, text_position[1] + 10), wrapped_text, font=font, fill="black")

        # Calculate position in the new image
        x_offset = (i % panels_horizontal) * (image_width + 2 * border_size)
        y_offset = (i // panels_horizontal) * (image_height + 2 * border_size + text_height)
        new_image.paste(panel, (x_offset, y_offset))

    # Save the new comic strip image
    return new_image
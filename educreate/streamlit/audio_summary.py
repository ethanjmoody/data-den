import os
import tiktoken
import yt_dlp

import streamlit as st

from keys import openai_token
from openai import OpenAI
from pydub import AudioSegment

client = OpenAI(api_key = openai_token)
openai_model = "gpt-4o-mini"

def count_tokens(text, model=openai_model):
  # Load the appropriate tokenizer for the model
  encoding = tiktoken.encoding_for_model(model)
  # Encode the text to get the tokens
  tokens = encoding.encode(text)
  # Return the number of tokens
  return len(tokens)

# Function to extract audio from any YouTube video
def extract_audio_from_yt(youtube_path, output_path):
  
  ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',}],
      'outtmpl': output_path
      }

  print(output_path)
  if os.path.exists(output_path + '.mp3'):
    os.remove(output_path + '.mp3') 
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_path])
        metadata = ydl.extract_info(youtube_path, download= False)
        length = metadata['duration']
  else:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_path])
            metadata = ydl.extract_info(youtube_path, download= False)
            length = metadata['duration']
  return length    

# Function to extract audio from any video
def extract_audio_from_video(video_path, audio_output_path):
  print(video_path)
  video = AudioSegment.from_file(video_path, format="mp4")
  length = len(video)
  video.export(audio_output_path, format="mp3")
  return length

def extract(type, url, user_prompt):
    if type == "YouTube":
        audio_output_path = '/content/yt_audio'
        length = extract_audio_from_yt(url, audio_output_path)
        print("length: ", length)
        load_audio_path = audio_output_path + '.mp3'
    else:
        audio_output_path = '/content/vid_audio.mp3'
        length = extract_audio_from_video(url, audio_output_path)
        load_audio_path = audio_output_path

    increment = 8 #increment value in minutes
    a = list(range(0, length*1000, increment*1000*60))
    b = list(range(increment*1000*60, length*1000 + increment*1000*60, increment*1000*60))
    splits = list(zip(a,b))

    full_trans = ''
    for i in splits:
        print("i is:", i)
        full_file = AudioSegment.from_mp3(load_audio_path)
        file_seg = full_file[i[0]:i[1]]
        file_seg.export("intermediate.mp3", format="mp3")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=open('intermediate.mp3', 'rb')
        )
        print(transcription.text)
        full_trans += ' ' + transcription.text

    num_tokens = count_tokens(full_trans)

    if num_tokens < 128000:
        pass
    else:
        summ_transcription = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": """Summarize the text to be LESS THAN 25000 words."""},
                {"role": "user", "content": [{"type": "text", "text": f"Here is the text: {full_trans}"}]}
                ],
            temperature=0)
        full_trans = summ_transcription

    system_context = """
    You are a high school History teacher and an expert in a broad range of History topics.
    You will be provided with an audio transcription of the lesson taught by your fellow teaching colleague.
    You will also be given some instructions by your teaching colleague on the help required.
    Please ONLY provide your responses to the questions or instructions. DO NOT add responses such as 'Of Course, Certainly etc.'
    Here are the instructions from your teaching colleague:""" + user_prompt

    response = client.chat.completions.create(
        model=openai_model,
        messages=[
        {"role": "system", "content": system_context},
        {"role": "user", "content": [{"type": "text", "text": f"Here is the audio transcription of the lesson: {transcription.text}"}]}
        ],
        temperature=0)

    return response.choices[0].message.content

@st.cache_resource
def setup_pipeline(user_session_id):
    st.session_state['transcription'] = ""
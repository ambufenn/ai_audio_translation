from http.client import responses

import streamlit as st
from config import set_environment_variables
from groq import Groq
import os
# Set the environment variables
set_environment_variables()

# Now initialize the client
client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
)

def translate_audio(audio_file):
    response = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
    )
    return response

def get_groq(text, translated_text):
    prompt = f"(text) -> (translated_text)"
    chat_response = client.chat.completions.create(
        model= "llama-3.3-70b-versatile",
        messages= {"role": "user", "content": prompt},

    )
    return chat_response.choices[0].message.content

st.title("Aplikasi intrepretasi audio")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "mp4"])
if uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    text_to_ask = st.text_input("what will you ask?")
    try:
        translate_text = translate_audio(uploaded_file)
        st.subheader("translate text")
        st.write(translate_text)


        groq_response = get_groq(text_to_ask, translated_text)
        st.subheader("Groq Response")
        st.write(test_to_ask)
        st.write(groq_response)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload an audio file to get started")





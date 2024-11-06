import os
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import pyaudio
import wave

# Configure API key from environment variable or directly
api_key = "AIzaSyBi-G4VBxvLs3-nil4tuRYXCtM9q1BgW1o"
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Streamlit app
st.set_page_config(page_title="SKY HEIGHTS ACADEMY", page_icon="https://skyheightsacademy.com/wp-content/uploads/2016/06/DSC09664.jpg")

# Custom CSS for better styling and background image
st.markdown("""
    <style>
    .main {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        position: relative;
        background-image: url('https://skyheightsacademy.com/wp-content/uploads/2016/06/DSC09664.jpg');
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
    }
    .message {
        margin: 10px 0;
        padding: 10px;
        border-radius: 10px;
        word-wrap: break-word;
        overflow-wrap: break-word;
        background-color: rgba(255, 255, 255, 0.9);
    }
    .user-message {
        background-color: rgba(209, 231, 221, 0.9);
        border: 1px solid #0f5132;
        color: #0f5132;
        text-align: left;
        display: inline-block;
        max-width: 100%;
    }
    .model-message {
        background-color: rgba(207, 226, 255, 0.9);
        border: 1px solid #084298;
        color: #084298;
        text-align: left;
        display: inline-block;
        max-width: 100%;
        overflow-x: auto;
        overflow-y: auto;
        min-height: 50px;
        max-height: 400px;
    }
    .model-message img {
        margin-right: 10px;
    }
    .message p {
        margin: 0;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    .separator {
        margin: 10px 0;
        border-top: 1px solid #ccc;
    }
    .header, .footer {
        text-align: center;
        font-weight: bold;
        padding: 20px;
        background-color: #6c757d;
        color: white;
        border-radius: 10px;
    }
    .footer {
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <img src="https://skyheightsacademy.com/wp-content/uploads/2016/06/logo.png" width=200>
    <h1>SKY HEIGHTS ACADEMY</h1>
    <p>WELCOME TO SKY HEIGHTS ACADEMY, HOW CAN WE HELP YOU?</p>
</div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
    return ""

# Function to send message
def send_message(user_input):
    st.session_state.history.append({"role": "user", "content": user_input})

    # Correct the structure of the history
    formatted_history = [
        {"role": message["role"], "parts": [{"text": message["content"]}]}
        for message in st.session_state.history
    ]

    # Start a chat session and send the message
    chat_session = model.start_chat(history=formatted_history)
    response = chat_session.send_message(user_input)

    st.session_state.history.append({"role": "model", "content": response.text})

    # Convert response to speech
    tts = gTTS(response.text)
    tts.save("response.mp3")
    st.audio("response.mp3")

# Display chat history
for idx, message in enumerate(st.session_state.history):
    if message["role"] == "user":
        st.markdown(f"""
        <div class="message user-message">
            <p><strong>You:</strong> {message['content']}</p>
        </div>
        <div class="separator"></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message model-message" style="min-height: 60px; max-height: 400px; overflow-x: auto; overflow-y: auto;">
            <img src="https://skyheightsacademy.com/wp-content/uploads/2016/06/logo.png" width=20>
            <p><strong>SKY HEIGHTS ACADEMY:</strong> {message['content']}</p>
        </div>
        <div class="separator"></div>
        """, unsafe_allow_html=True)

# Input area
st.text_area("Type your message here and press Enter:", key='user_input', on_change=lambda: send_message(st.session_state.user_input), height=20)

# Voice input button
if st.button("Talk"):
    user_input = recognize_speech()
    if user_input:
        send_message(user_input)

# Footer
st.markdown("""
<div class="footer">
    <p>SKY HEIGHTS ACADEMY.BOT</p>
</div>
""", unsafe_allow_html=True)

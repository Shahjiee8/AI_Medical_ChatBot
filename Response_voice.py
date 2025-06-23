# Setup Text to Speech TTS (gtts) and use Pygame for Voice output
import os
import gradio as gr
import tempfile
from API_Config import client


def text_to_speech(input_text):
    """Generate an audio file from given text using Groq's TTS service.

    Args:
        input_text (str): The text to be converted to speech.

    Returns:
        str: The path to the generated audio file.

    Raises:
        gr.Error: if the TTS service is temporarily unavailable.
    """
    try:
        # Create speech synthesis request with Groq's TTS service
        response = client.audio.speech.create(
            model="playai-tts",
            voice="Aaliyah-PlayAI",
            response_format="mp3",
            input=input_text
        )

        # Get the audio data
        mp3_data = response.read()

        # Create a temporary file to store the audio data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tmpfile.write(mp3_data)
            tmpfile_path = tmpfile.name

        # Return the path to the temporary file
        return tmpfile_path
    except Exception:
        # If there is any error, raise a gr.Error, indicating that the AI service is unavailable
        raise gr.Error("Sorry, our AI service is temporarily unavailable.")

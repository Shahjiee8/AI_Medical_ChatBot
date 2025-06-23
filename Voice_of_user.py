import gradio as gr
import os
from API_Config import client


def transcription_with_groq(stt_model, audio_data):
    """Transcribes audio data using the specified speech-to-text model.

    Args:
        stt_model (str): The speech-to-text model to use for transcription.
        audio_data (file-like object): The audio data to transcribe.

    Returns:
        str: The transcribed text from the audio data.

    Raises:
        gr.Error: If the transcription service is temporarily unavailable.
    """
    try:
        # Attempt to create a transcription using the specified model and audio data
        transcription = client.audio.transcriptions.create(
            model=stt_model,  # Specify the model for transcription
            file=audio_data,  # Provide the audio file for transcription
            language="en"     # Set the language to English
        )
        return transcription.text  # Return the transcribed text
    except Exception:
        # Raise an error if the transcription service is unavailable
        raise gr.Error("Sorry, our AI service is temporarily unavailable.")

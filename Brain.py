import os
from Voice_of_user import transcription_with_groq
from Response_voice import text_to_speech
from io import BytesIO
import gradio as gr
import base64
import random
from PIL import Image
import urllib.parse
from API_Config import client


def encode_image(image_path):
    """
    Tries to open an image file from the specified file path and
    encodes it to a base64 string.

    Args:
        image_path (str): The file path to the image to be encoded.

    Returns:
        str: The base64 encoded string representation of the image.

    Raises:
        gr.Error: If the encoding fails for any reason.
            - If the image file is not found, raises a FileNotFoundError.
            - If any other exception occurs during encoding, raises a
              generic gr.Error.
    """
    try:
        # Try to open the image file
        with open(image_path, "rb") as image_file:
            # Encode the image to base64
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        # If the image file is not found, raise a FileNotFoundError
        raise gr.Error(f"Image file not found: {image_path}")
    except Exception as e:
        # If any other exception occurs, raise a generic gr.Error
        raise gr.Error(f"Error encoding image: {e}")


def base64_to_pil(b64_string):
    """
    Decodes a base64 encoded string to a PIL Image object.

    Args:
        b64_string (str): The base64 encoded string representation of the image.
            This string is expected to be a valid base64 encoded string.
            If the string starts with "data:image/", it is assumed to be a
            data URI and the data is extracted from the string.

    Returns:
        PIL.Image: The decoded PIL Image object.

    Raises:
        gr.Error: If the conversion fails for any reason.
            This can happen if the input string is not a valid base64 encoded
            string, or if the image data is corrupted.
    """
    try:
        if b64_string.startswith("data:image"):
            # Extract the data from the data URI
            b64_string = b64_string.split(",")[1]
        # Decode the base64 string to bytes
        image_data = base64.b64decode(b64_string)
        # Use PIL to open the image from the bytes
        return Image.open(BytesIO(image_data))
    except Exception as e:
        # Raise an error if anything goes wrong
        raise gr.Error(f"Error decoding base64 string to PIL Image: {e}")


def analyze_image(query, analyzing_model, encoded_image=None):
    """
    Analyzes an image using a specified model and generates a text response based on the input query.

    Args:
        query (str): The user's query.
        analyzing_model (str): The model to use for image analysis.
        encoded_image (str): The base64 encoded string representation of the image to analyze.

    Returns:
        str: The response as a string.

    Raises:
        gr.Error: If the analyzing fails for any reason.
    """
    try:
        # Build the input data for the chat completion
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": query}]
            }
        ]
        if encoded_image:
            # Add the image to the input data if it's provided
            messages[0]["content"].append({
                "type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
            })
        # Call the chat completion API
        chat_completion = client.chat.completions.create(messages=messages, model=analyzing_model)
        # Return the response text
        return chat_completion.choices[0].message.content
    except Exception:
        # Raise an error if anything goes wrong
        raise gr.Error("Sorry, our AI service is temporarily unavailable.")


def generate_stt_and_images(multimodal_input):
    """
    Processes multimodal input to generate speech-to-text (STT) and image encodings.

    Args:
        multimodal_input (dict or str): The input data, which can be a dictionary containing 'text' and 'files' keys,
                                        or a string.

    Returns:
        tuple: A tuple containing:
            - str: The transcribed text from audio input, if available.
            - str: The base64 encoded string of the image, if available.
            - str: The URL of the image, if available.

    Raises:
        gr.Error: If the transcription or encoding services are temporarily unavailable.
    """
    stt = ""
    encoded_image = None
    image_url = None

    if isinstance(multimodal_input, dict):
        # If the input is a dictionary, check for text and files
        if multimodal_input.get("text"):
            stt = multimodal_input["text"].strip()

        files = multimodal_input.get("files", [])
        for file_path in files:
            # Check if the file is an audio file
            if file_path.lower().endswith(('.mp3', '.wav')) and not stt:
                try:
                    # Transcribe the audio using Groq
                    with open(file_path, "rb") as audio_file:
                        stt = transcription_with_groq("whisper-large-v3-turbo", audio_data=audio_file)
                except Exception:
                    raise gr.Error("Sorry, our AI service is temporarily unavailable.")

            # Check if the file is an image file
            elif file_path.lower().endswith(('.jpg', '.jpeg', '.png')) and not encoded_image:
                try:
                    # Encode the image to a base64 string
                    encoded_image = encode_image(file_path)
                except Exception:
                    raise gr.Error("Sorry, our AI service is temporarily unavailable.")

    elif isinstance(multimodal_input, str):
        # If the input is a string, just strip it
        stt = multimodal_input.strip()

    # If we don't have an image, and we have text, generate an image
    if not encoded_image and stt:
        prompt_suffix = """You are an image prompt generator. Based on the medical condition provided, generate a 
        **short, descriptive image prompt** of **5 to 6 words**, with no explanation or extra text. **Only return 
        the prompt**. Do not include quotes, punctuation, or any introductory text."""
        try:
            # Call the chat completion API
            response = client.chat.completions.create(
                model="compound-beta-mini",
                messages=[{"role": "user", "content": stt + prompt_suffix}]
            )
            # Get the generated image prompt
            selected_prompt = response.choices[0].message.content

            # Generate an image using the image generation API
            width, height = 256, 256
            model = 'flux'
            seed = random.randint(0, 999999)
            nologo = "true"
            encoded_prompt = urllib.parse.quote(selected_prompt)
            image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed={seed}&model={model}&nologo={nologo}"
        except Exception:
            raise gr.Error("Sorry, our AI service is temporarily unavailable.")

    # Return the transcribed text, the encoded image, and the image URL
    return stt, encoded_image, image_url


def query_func(stt, encoded_image, image_url):
    """
    Generates a response to a user query based on the input text and/or image.

    Args:
        stt (str): The transcribed text from audio input, if available.
        encoded_image (str): The base64 encoded string of the image, if available.
        image_url (str): The URL of the image, if available.

    Returns:
        - str: The response as a string.
        - str: The image to display, either as a base64 encoded string or a URL.

    Raises:
        gr.Error: If the analyzing or encoding services are temporarily unavailable.
    """
    try:
        # Determine the image to display based on availability of encoded image
        if encoded_image:
            # Convert base64 string to a PIL image for display
            image_display = base64_to_pil(encoded_image)
            # Use the encoded image for reporting
            report_image = encoded_image
        else:
            # Use the image URL for display if no encoded image is available
            image_display = image_url
            # Use the image URL for reporting
            report_image = image_url
    except Exception:
        # Raise an error if there is an issue with image processing
        raise gr.Error("Sorry, our AI service is temporarily unavailable.")

    # Return the speech-to-text result, the image for display, and the image for reporting
    return stt, image_display, report_image


def generate_response(stt, img_to_display):
    """
    Generates a response to a user query based on the input text and/or image.

    Args:
        stt (str): The transcribed text from audio input, if available.
        img_to_display (str): The image to display, either as a base64 encoded string or a URL.

    Returns:
        - str: The response as a string.
        - str: The audio file to play, as a path to the file.

    Raises:
        gr.Error: If the analyzing or encoding services are temporarily unavailable.
    """
    if not stt:
        # Default message if speech-to-text is unavailable
        stt = "I'm sorry, I couldn't understand your speech clearly. Please try again."

    # System prompt for image analysis
    system_prompt = """You are a professional doctor, providing educational advice. Analyze the provided image 
    (or description) and determine if there are any visible medical concerns. If applicable, suggest possible 
    differentials and remedies. Respond naturally, in 5 to 6 lines, without using numbers, special characters, 
    markdown formatting, or any AI disclaimers. Speak directly to the user as if you are a real doctor. If an input 
    description is provided, start with 'Based on your description...', if the provided image appears to be AI generated 
    handle it by saying something like 'I have an image here...' and then follow up with 'if your condition is like 
    this then...', if no input is provided, say 'Please upload an image or provide a description of your condition.' 
    If you are unsure about the input, politely ask the user for clarification. Start your answer immediately, with 
    no preamble."""

    # Analyze the image if provided
    if img_to_display:
        try:
            # Call analyze_image with the system prompt and image
            response_text = analyze_image(
                query=system_prompt + stt,
                analyzing_model="meta-llama/llama-4-maverick-17b-128e-instruct",
                encoded_image=img_to_display)
        except Exception:
            # Raise an error if image analysis fails
            raise gr.Error("Sorry, our AI service is temporarily unavailable.")
    else:
        try:
            # Call analyze_image with only the system prompt
            response_text = analyze_image(
                query=system_prompt + stt,
                analyzing_model="meta-llama/llama-4-maverick-17b-128e-instruct")
        except Exception:
            # Raise an error if image analysis fails
            raise gr.Error("Sorry, our AI service is temporarily unavailable.")

    try:
        # Convert response text to speech
        audio_data = text_to_speech(input_text=response_text)
    except Exception:
        # Raise an error if text-to-speech conversion fails
        raise gr.Error("Sorry, our AI service is temporarily unavailable.")

    # For history tracking
    for_history = response_text

    return audio_data, response_text, for_history


def generate_followup_response(multimodal_input, history):
    """
    Generate a response to a user query based on the input text and/or image.

    Args:
        multimodal_input (dict): A dictionary containing the user's query.
            The dictionary should contain the following keys:
                - text (str): The user's query as a string.
                - files (list): A list of file paths to the audio/image files.
                - image_url (str): The URL of the image.
        history (str): The conversation history.

    Returns:
        list: The updated conversation history.
        str: The response as a string.

    Raises:
        gr.Error: If the analyzing or encoding services are temporarily unavailable.
    """
    followup_his = [{"role": "assistant", "content": history}]

    try:
        user_query = ""

        if isinstance(multimodal_input, dict):
            # Check for direct text input
            if multimodal_input.get("text"):
                user_query = multimodal_input["text"].strip()

            # Process audio files if present
            files = multimodal_input.get("files", [])
            for file_path in files:
                if file_path.lower().endswith(('.mp3', '.wav')) and not user_query:
                    try:
                        with open(file_path, "rb") as audio_file:
                            user_query = transcription_with_groq("whisper-large-v3-turbo", audio_file)
                    except FileNotFoundError:
                        return followup_his, "Audio file not found. Please try again."
                    except Exception:
                        return followup_his, "Error transcribing audio. Please try again."
        elif isinstance(multimodal_input, str):
            # Handle simple string input
            user_query = multimodal_input.strip()

        if not user_query:
            # Return error if no valid input is found
            return followup_his, "I couldn't understand your input. Could you please try again?"

        # Append user input to conversation history
        followup_his.append({"role": "user", "content": user_query})

        # Clean and format chat history for processing
        clean_history = []
        for msg in followup_his:
            content = msg.get("content", "")
            if not isinstance(content, str):
                content = str(content)
            clean_history.append({
                "role": msg.get("role", "user"),
                "content": content
            })

        try:
            # Generate a response using the chat model
            response = client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                messages=clean_history
            )
            reply = response.choices[0].message.content.strip()
            followup_his.append({"role": "assistant", "content": reply})

            return clean_history, reply
        except Exception:
            # Handle errors during response generation
            raise gr.Error("Sorry, something went wrong while generating a response.")

    except Exception:
        # Handle unforeseen processing errors
        raise gr.Error("Sorry, something went wrong while processing your follow-up.")

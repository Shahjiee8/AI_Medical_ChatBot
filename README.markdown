# Dr. Chat - AI-Powered Health Assistant

Dr. Chat is an intelligent, voice-driven health companion designed to assist users by analyzing symptoms through text, voice, or image inputs. Powered by advanced AI models, it provides educational medical advice, generates professional medical reports, and offers a user-friendly interface built with Gradio. The application integrates with Firebase for user authentication and data storage, and leverages Groq's API for speech-to-text, text-to-speech, and language processing.

## Features

- **Multimodal Input**: Accepts text, audio (via speech-to-text), and images for symptom analysis.
- **AI-Driven Responses**: Generates educational medical advice using Groq's language models, mimicking a professional doctor's tone.
- **Medical Reports**: Creates structured PDF reports with symptoms, observations, and recommendations, including embedded images.
- **User Authentication**: Supports login, signup, and guest access via Firebase Authentication and Firestore.
- **Interactive UI**: Polished Gradio interface with a custom Ocean theme, supporting dynamic section toggling and responsive design.
- **Report History**: Stores up to 5 recent reports per user, accessible via a sidebar.
- **Voice Interaction**: Converts AI responses to speech for an accessible user experience.

## Project Structure

- **`gradio_ui.py`**: Main file defining the Gradio interface, handling UI logic and interactions.
- **`API_Config.py`**: Configures API keys and initializes Groq, Firebase, and APITemplate.io services.
- **`Brain.py`**: Core logic for processing multimodal inputs, generating responses, and analyzing images.
- **`Database.py`**: Manages user authentication and report storage using Firebase.
- **`report.py`**: Generates and stores medical reports in PDF format.
- **`Response_voice.py`**: Handles text-to-speech conversion using Groq's TTS service.
- **`ui_config.py`**: Defines UI theme, landing page text, and custom CSS/JS styling.
- **`Voice_of_user.py`**: Processes speech-to-text transcription using Groq's API.

## Prerequisites

- Python 3.8 or higher
- Firebase project with Authentication and Firestore enabled
- Groq API key for AI services
- APITemplate.io API key for PDF generation
- Service account key JSON file for Firebase Admin SDK

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/dr-chat.git
   cd dr-chat
   ```

2. **Install Dependencies**:
   Create a virtual environment and install the required Python packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Sample `requirements.txt`:
   ```
   gradio==4.44.0
   firebase-admin==6.5.0
   pyrebase==3.0.27
   groq==0.11.0
   pillow==10.4.0
   requests==2.32.3
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add the following:
   ```bash
   PDF_API_KEY=your_apitemplate_io_api_key
   GROQ_API_KEY=your_groq_api_key
   PYREBASE_API_KEY=your_firebase_api_key
   ```

4. **Configure Firebase**:
   - Download your Firebase service account key JSON file and place it in a secure location (e.g., `C:\Users\your_username\Downloads\serviceAccountKey.json`).
   - Update the path in `API_Config.py`:
     ```python
     cred = credentials.Certificate(r"path\to\serviceAccountKey.json")
     ```

5. **Run the Application**:
   Launch the Gradio interface:
   ```bash
   python gradio_ui.py
   ```
   The app will open in your default browser (`inbrowser=True`) with debug mode enabled (`debug=True`).

## Usage

1. **Landing Page**:
   - Click "Get Started" to access the login or guest mode.

2. **Login/Signup**:
   - Log in with an existing account, sign up for a new account, or continue as a guest.
   - Guest mode allows limited access to the main interface without report generation.

3. **Main Interface**:
   - Use the "Main" tab to input queries via text, microphone, or image uploads.
   - View transcribed text, generated images, and AI responses (text and audio).
   - Click "Clear" to reset inputs.

4. **Follow-Up**:
   - Use the "Follow Up" tab to ask additional questions based on previous responses.
   - Generate a medical report using the "Generate Medical Report" button.

5. **Reports**:
   - Access the "Report" tab to preview and download PDF reports.
   - View up to 5 recent reports in the sidebar (for logged-in users).

6. **Logout**:
   - Click "Logout" in the sidebar to return to the login page.

## Configuration

- **UI Styling** (`ui_config.py`):
  - Custom Ocean theme with teal and blue hues.
  - CSS for responsive section containers and hidden footer.
  - JavaScript to enforce light mode.

- **Firebase** (`API_Config.py`):
  - Configured for Authentication and Firestore.
  - Stores user data and reports in the "Patients" collection.

- **Groq API** (`Brain.py`, `Voice_of_user.py`, `Response_voice.py`):
  - Uses `whisper-large-v3-turbo` for speech-to-text.
  - Uses `playai-tts` with Aaliyah voice for text-to-speech.
  - Uses `meta-llama/llama-4-maverick-17b-128e-instruct` for response generation and `compound-beta-mini` for image prompt generation.

- **PDF Generation** (`report.py`):
  - Uses APITemplate.io with template ID `db277b23f34421f2`.
  - Generates reports with embedded images and stores them in Firestore.

## Security Notes

- Store API keys and Firebase credentials securely, avoiding version control.
- Ensure the Firebase service account key file is protected and not publicly accessible.
- Consider adding password strength validation in `Database.py`.

## Limitations

- **Guest Mode**: Limited functionality (e.g., no report generation).
- **Language Support**: Speech-to-text is currently English-only.
- **AI Accuracy**: Responses are educational and should not replace professional medical advice.
- **Temporary Files**: Text-to-speech generates temporary MP3 files without automatic cleanup.

## Future Improvements

- Add loading indicators for API calls.
- Implement password strength validation.
- Support multilingual speech-to-text.
- Optimize image processing for large files.
- Add unit tests and error logging.
- Improve mobile responsiveness and accessibility.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or support, contact [your-email@example.com](mailto:your-email@example.com).
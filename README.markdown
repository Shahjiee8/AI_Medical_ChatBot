# AI Medical ChatBot

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-UI-blueviolet)](https://www.gradio.app/)

## Overview

**AI Medical ChatBot** is an intelligent, voice-driven health companion designed to assist users with medical queries, symptom analysis, and health insights. Powered by advanced AI models, it mimics the clarity and compassion of real healthcare professionals while providing educational advice. Users can interact via voice, text, or images to describe symptoms, receive differential diagnoses, suggestions, and even generate personalized medical reports.

This project leverages multimodal AI capabilities (text, audio, and vision) to make healthcare more accessible. It includes user authentication, conversation history, and secure report storage using Firebase. The chatbot emphasizes that it is for educational purposes only and is not a substitute for professional medical advice.

Key highlights:
- **Voice-to-Text Transcription**: Convert spoken symptoms into text using Groq's Whisper model.
- **Image Analysis**: Upload images for visual symptom analysis (e.g., skin conditions).
- **Conversational AI**: Maintain follow-up dialogues with context-aware responses.
- **Report Generation**: Create downloadable PDF reports with symptoms, observations, and recommendations.
- **User Management**: Secure login/register with Firebase, and persistent report history.

The app is built with Gradio for an intuitive web interface and runs locally or deployable to platforms like Hugging Face Spaces.

## Features

- **Multimodal Input**: Supports text, audio (MP3/WAV), and images (JPG/PNG) for queries.
- **AI-Powered Analysis**: Uses Llama models for medical reasoning and Flux for image generation (if no image provided).
- **Text-to-Speech Output**: Responses are voiced back using Groq's TTS for a natural experience.
- **User Authentication**: Register/login with email/password via Firebase Auth.
- **Report Management**: Generate, preview, and download PDF reports; store up to 5 latest reports per user.
- **Guest Mode**: Continue without login for quick queries.
- **Responsive UI**: Themed interface with sections for landing, login, main chat, follow-ups, and reports.
- **Error Handling**: Graceful fallbacks for unavailable services (e.g., AI API downtime).
- **Privacy-Focused**: No sensitive data stored beyond user consent; reports are user-specific.

## Demo

A live demo is available [here](https://huggingface.co/spaces/Shahjiee8/AI_Medical_ChatBot) (if deployed; otherwise, run locally).

Example workflow:
1. User says or types: "I have a rash on my arm."
2. Bot transcribes/analyzes and responds: "Based on your description, it could be an allergic reaction. Upload an image for better analysis."
3. User uploads image → Bot suggests differentials and remedies.
4. Generate report → Download PDF with structured insights.

## Prerequisites

- Python 3.8 or higher
- API Keys:
  - Groq API Key (for AI models and TTS/STT): Sign up at [Groq Console](https://console.groq.com/).
  - Firebase Project (for Auth and Firestore): Set up at [Firebase Console](https://console.firebase.google.com/).
  - APITemplate.io API Key (for PDF generation): Sign up at [APITemplate](https://apitemplate.io/).
- Firebase Service Account JSON (for admin SDK): Download from Firebase Console > Project Settings > Service Accounts.
- Basic knowledge of environment variables and virtual environments.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Shahjiee8/AI_Medical_ChatBot.git
   cd AI_Medical_ChatBot
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install required packages via pip. Create a `requirements.txt` file if needed (generated from the code):
   ```
   gradio
   groq
   firebase-admin
   pyrebase4
   pillow
   requests
   firebase-admin
   ```
   Then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (or set via OS environment):
   ```
   GROQ_API_KEY=your_groq_api_key_here
   PYREBASE_API_KEY=your_firebase_web_api_key_here
   PDF_API_KEY=your_apitemplate_api_key_here
   ```
   - For Firebase Service Account: Place `serviceAccountKey.json` in the project root (path: `C:\Users\your_username\Downloads\serviceAccountKey.json` – update in `API_Config.py` if needed).

5. **Firebase Setup**:
   - Create a Firebase project named "ai-medical-chatbot-e33f2" (or update config in `API_Config.py`).
   - Enable Authentication (Email/Password) and Firestore Database.
   - Update `firebaseConfig` in `API_Config.py` with your project's details.

6. **Run the Application**:
   ```bash
   python gradio_ui.py
   ```
   The Gradio interface will launch in your browser (debug mode enabled for verbose output). Access at `http://127.0.0.1:7860`.

## Project Structure

The project is modular, with separation of concerns for UI, backend logic, database, and utilities:

```
AI_Medical_ChatBot/
├── Brain.py                  # Core AI logic: STT, image encoding, analysis, response generation, follow-ups.
├── Database.py               # Firebase Auth and Firestore operations: register, login, report storage.
├── gradio_ui.py              # Main Gradio interface: UI components, event handlers, state management.
├── report.py                 # PDF report generation using APITemplate.io and AI summarization.
├── Voice_of_user.py          # Speech-to-Text transcription using Groq Whisper.
├── Response_voice.py         # Text-to-Speech using Groq TTS.
├── API_Config.py             # Configuration: API keys, Firebase init, Groq client.
├── ui_config.py              # UI themes, CSS, JS, and landing page content.
├── landing_page_image.jpg    # Static image for landing page (add your own).
├── serviceAccountKey.json    # Firebase service account (git ignore this!).
├── .env                      # Environment variables (git ignore).
├── requirements.txt          # Python dependencies.
└── README.md                 # This file.
```

- **Key Files Breakdown**:
  - `Brain.py`: Handles multimodal inputs (audio/text/image), generates prompts for AI, and orchestrates responses.
  - `Database.py`: Manages user registration/login and retrieves/stores reports in Firestore.
  - `gradio_ui.py`: Defines the Gradio Blocks, sections (landing, login, main, etc.), and click/submit events.
  - `report.py`: Extracts conversation history, generates JSON-structured reports, and creates PDFs.
  - Utilities: `Voice_of_user.py` and `Response_voice.py` for audio I/O; `ui_config.py` for styling.

## Usage

1. **Launch the App**: Run `python gradio_ui.py` and navigate to the local URL.
2. **Landing Page**: Read the intro and click "Get Started".
3. **Login/Register**: Use email/password or continue as guest.
4. **Main Chat**:
   - Type or record audio for symptoms (e.g., "I have a headache").
   - Upload an image for visual analysis.
   - Receive voiced/text response with advice.
5. **Follow-Ups**: Ask clarifying questions in the dedicated section.
6. **Generate Report**: Click the report button to preview and download a PDF (stored in Firebase for logged-in users).
7. **Logout**: Return to login; reports history shown in sidebar.

**Notes**:
- Images are analyzed for medical concerns; AI-generated images are handled gracefully.
- Reports include patient details, image, and structured sections (Symptoms, Observations, Recommendations).
- Limit: Only latest 5 reports stored per user to manage storage.

## Technologies Used

- **Frontend/UI**: Gradio (Python-based web UI framework).
- **AI/ML**: Groq (for Llama models, Whisper STT, TTS, Flux image gen).
- **Backend/Database**: Firebase (Auth, Firestore for user data/reports).
- **PDF Generation**: APITemplate.io API.
- **Image Processing**: PIL (Python Imaging Library).
- **Other**: Requests (HTTP), Base64 encoding, Tempfile for audio handling.
- **Deployment**: Local (Gradio server); scalable to Hugging Face or Vercel.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

**Guidelines**:
- Ensure code adheres to PEP 8 style.
- Add tests for new features (e.g., unit tests for AI prompts).
- Update documentation (this README) for changes.
- Respect privacy: No real medical data in examples.

Issues? Open a GitHub issue with details.

## Acknowledgments

- Gradio for the seamless UI.
- Groq for fast AI inference.
- Firebase for scalable backend.
- APITemplate.io for PDF templating.

## Disclaimer

This chatbot is for **educational and informational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for health concerns. The developers are not liable for any misuse or outcomes.

---

*Built with ❤️ by Shahjiee8. Last updated: September 07, 2025.*

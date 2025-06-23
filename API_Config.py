import os
import firebase_admin
from firebase_admin import credentials, firestore
from pyrebase import pyrebase
from groq import Groq
import gradio as gr
import json

# APITemplate Config
try:
    PDF_API_KEY = os.environ["PDF_API_KEY"]
except KeyError:
    raise gr.Error("PDF_API_KEY environment variable not set.")
template_id = "db277b23f34421f2"

# Groq client Config
try:
    GROQ_API_KEY = os.environ["GROQ_API_KEY"]
except KeyError:
    raise gr.Error("GROQ_API_KEY environment variable not set.")
client = Groq(api_key=GROQ_API_KEY)

# Firebase Config
try:
    PYREBASE_API_KEY = os.environ["PYREBASE_API_KEY"]
except KeyError:
    raise gr.Error("PYREBASE_API_KEY environment variable not set.")
firebaseConfig = {
  "apiKey": PYREBASE_API_KEY,
  "authDomain": "ai-medical-chatbot-e33f2.firebaseapp.com",
  "projectId": "ai-medical-chatbot-e33f2",
  "storageBucket": "ai-medical-chatbot-e33f2.firebasestorage.app",
  "messagingSenderId": "421207447431",
  "appId": "1:421207447431:web:87a7c6b8c31853a5596522",
  "databaseURL": ""
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Firebase_admin Config
try:
    cred = credentials.Certificate(r"C:\Users\adils\Downloads\serviceAccountKey.json")
except ValueError:
    raise gr.Error("FIREBASE_CERTIFICATE environment variable is not a valid JSON.")
firebase_admin.initialize_app(cred)

db = firestore.client()

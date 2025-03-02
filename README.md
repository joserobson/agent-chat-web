# Agent Chat Web Application

This project is a simple web application for chatting with an AI agent, featuring audio transcription.  It uses a Flask backend and a JavaScript frontend for a user-friendly experience.

## Features

* **Text Chat:**  Send and receive text messages. The bot currently provides a basic echo response, easily expandable to integrate with a sophisticated AI chatbot API.
* **Audio Transcription:** Record audio messages and send them for transcription using an external API (currently Groq API, but easily adaptable).  The transcribed text is displayed in the chat.
* **WhatsApp-Inspired UI:** The frontend is designed with a clean and intuitive interface, similar to WhatsApp's chat style.

## Technologies

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, JavaScript
* **Transcription API:** Groq (easily replaceable with others like AssemblyAI or Google Cloud Speech-to-Text)

## Setup

1. **Prerequisites:**
   - Python 3.x installed
   - `pip` (Python package installer)
   - A Groq API account and API key (if using Groq; otherwise, an account with your chosen transcription service)

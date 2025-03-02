from flask import Flask, request, jsonify
import requests
import os
import logging
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace with your Groq API endpoint and key
GROQ_API_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_API_KEY = "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"

@app.route("/")
def index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("index.html not found.")
        return "index.html not found", 404
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred", 500
    
@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        logger.error("No audio file provided.")
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files["audio"]
    temp_path = "temp_audio.wav"
    audio_file.save(temp_path)
    logger.info("Audio file saved temporarily.")

    try:
        # Prepare the request to Groq API
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
        }
        with open(temp_path, "rb") as f:
            files = {
                "file": (temp_path, f),  # Pass tuple (filename, file object)
            }
            data = {
                "model": "whisper-large-v3",  # Specify the model
            }

            logger.info("Sending audio to Groq API...")
            response = requests.post(GROQ_API_URL, headers=headers, files=files, data=data)

        if response.status_code != 200:
            logger.error(f"Transcription failed. Status code: {response.status_code}, Response: {response.text}")
            return jsonify({"error": "Transcription failed."}), 500

        transcription = response.json().get("text")  # Groq API returns the transcription in the "text" field
        logger.info(f"Transcription successful: {transcription}")
        return jsonify({"transcription": transcription})
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        return jsonify({"error": "An error occurred during transcription."}), 500
    finally:
        # Clean up the temporary file
        retries = 3
        for attempt in range(retries):
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    logger.info("Temporary audio file removed.")
                break  # Success, exit the loop
            except PermissionError as e:
                if attempt < retries - 1:
                  logger.warning(f"Attempt {attempt + 1}/{retries}: PermissionError on temp_audio.wav, retrying in 1 second. Error: {e}")
                  time.sleep(1)
                else:
                  logger.error(f"Failed to delete temporary file temp_audio.wav after multiple retries: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred while deleting temporary file: {e}")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    logger.info(f"Received chat message: {message}")

    # Replace this with your chat logic (e.g., call Groq or another API)
    response = f"Bot: You said '{message}'"
    logger.info(f"Sending chat response: {response}")

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

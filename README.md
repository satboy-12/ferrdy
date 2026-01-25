# FERRDY - AI Voice Assistant

A personal AI assistant that combines face recognition, speech recognition, and voice response capabilities.

## Features

✨ **Face Authentication** - Secure face recognition using DeepFace
🎤 **Voice Commands** - Speak commands and FERRDY responds
🗣️ **Voice Replies** - All responses are spoken, not just text
🚀 **Multiple Commands** - Open apps, tell jokes, search web, and more

## Available Voice Commands

- **"open chrome"** - Opens Google Chrome browser
- **"open vs code"** - Opens Visual Studio Code
- **"open notepad"** - Opens Notepad
- **"tell me a joke"** - Tells a random programming joke
- **"what time is it"** - Tells current time
- **"what's the date"** - Tells current date
- **"search [query]"** - Searches Google (e.g., "search Python tutorials")
- **"health tip"** - Gives random health tips
- **"who are you"** - Introduction
- **"help"** - Lists all available commands
- **"exit"** or **"goodbye"** - Shuts down FERRDY

## Installation

### Prerequisites
- Python 3.8+
- Webcam (for face authentication)
- Microphone (for voice commands)
- Speaker (for voice replies)
- Internet connection (for Google Speech Recognition)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ferrdy.git
cd ferrdy
```

2. Create a virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Test Mode (No Face Authentication)
```bash
.\.venv\Scripts\python.exe ferrdy_main.py --test
```

### Normal Mode (With Face Authentication)
1. Add your face photo to the `faces/` folder as `yourname.jpg`
2. Run:
```bash
.\.venv\Scripts\python.exe ferrdy_main.py
```

## Project Structure

```
ferrdy/
├── face_auth.py           # Face recognition module
├── voice_assistant.py     # Voice command processing
├── ferrdy_main.py         # Main application
├── requirements.txt       # Python dependencies
├── faces/                 # Folder for storing face images
└── README.md             # This file
```

## Dependencies

- opencv-python - Computer vision
- deepface - Face recognition
- numpy - Numerical computing
- speechrecognition - Voice command recognition
- pyttsx3 - Text-to-speech
- pyaudio - Audio processing
- tensorflow - Deep learning
- tf-keras - Keras API

## Technology Stack

- **Face Recognition:** DeepFace with Facenet model
- **Speech Recognition:** Google Cloud Speech-to-Text API
- **Text-to-Speech:** pyttsx3
- **Computer Vision:** OpenCV
- **Deep Learning:** TensorFlow & Keras

## How It Works

1. **Face Authentication** - Uses DeepFace to extract face embeddings and verify identity
2. **Voice Recognition** - Captures audio and converts to text using Google Speech API
3. **Command Processing** - Matches voice input to available commands
4. **Voice Response** - Uses pyttsx3 to synthesize and play audio response
5. **Command Execution** - Opens applications or performs requested actions

## Troubleshooting

### No Microphone Detected
- Ensure microphone is connected and set as default input device
- Check Windows sound settings

### No Audio Output
- Check speaker volume and ensure speakers are connected
- Test with `test_voice.py`

### Face Authentication Fails
- Add clear face photos to `faces/` folder
- Ensure good lighting when authenticating

### Google Speech API Errors
- Check internet connection
- Speak clearly near the microphone

## License

MIT License - Feel free to use and modify!

## Author

Created by Sathya

## Support

For issues and feature requests, please open an issue on GitHub.

---

**Enjoy using FERRDY! Happy voice commanding!** 🎉

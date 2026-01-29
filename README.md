# FERRDY - AI Voice Assistant with GUI

A personal AI assistant with a modern graphical interface that combines face recognition, speech recognition, and voice response capabilities. Now featuring a beautiful tkinter GUI with a tabbed interface!

## ✨ Features

🎨 **Modern GUI Interface** - Tabbed tkinter application with dark theme
🔐 **Face Authentication** - Secure face recognition using DeepFace
🎤 **Voice Commands** - Speak commands and FERRDY responds
🗣️ **Voice Replies** - All responses are spoken
⚙️ **Customizable Settings** - Adjust face recognition threshold, test mode
📝 **Command History** - Real-time logging of all interactions
🧪 **Test Mode** - Skip face authentication for development
📦 **Standalone Executable** - FERRDY.exe ready to use without Python

## 🖥️ GUI Features

### Home Tab
- Face authentication with visual status indicators
- Voice command listening with animated indicator (🟢🔴 blinking)
- Quick command buttons (Chrome, VS Code, Health, Time, Date, Exit)
- Real-time command history with timestamps

### Settings Tab
- **Test Mode** - Skip face authentication for testing
- **Threshold Slider** - Adjust face recognition sensitivity (0.3 to 1.0)
- Audio settings display (microphone, speech rate, volume)
- About section with version and tech stack info

### Help Tab
- Complete documentation
- Voice command reference
- Troubleshooting guide
- Feature list and keyboard shortcuts

## 🚀 Quick Start

### Option 1: Run Standalone Executable (Recommended)
Simply download and run `FERRDY.exe` from the [releases page](https://github.com/satboy-12/ferrdy/releases)
- No Python installation needed
- All dependencies included
- Works on Windows 10/11

### Option 2: Run from Python

1. Clone the repository:
```bash
git clone https://github.com/satboy-12/ferrdy.git
cd ferrdy
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python ferrdy_main.py
```

## 🎤 Voice Commands

- **"open chrome"** - Opens Google Chrome browser
- **"open vs code"** - Opens Visual Studio Code
- **"open notepad"** - Opens Notepad
- **"health"** - Gives random health tips
- **"time"** - Tells current time
- **"date"** - Tells current date
- **"search [query]"** - Searches Google
- **"exit"** - Closes the application

## 📋 Prerequisites

### For Standalone .exe
- Windows 10/11
- Webcam (for face authentication)
- Microphone (for voice commands)
- Speaker (for voice replies)
- Internet connection (for Google Speech Recognition)

### For Python Source
- Python 3.8+
- Webcam, Microphone, Speaker
- Internet connection

## 📁 Project Structure

```
ferrdy/
├── ferrdy_gui.py          # GUI Application (tkinter)
├── ferrdy_main.py         # Entry point
├── face_auth.py           # Face recognition module
├── voice_assistant.py     # Voice command processing
├── FERRDY.spec            # PyInstaller configuration
├── requirements.txt       # Python dependencies
├── faces/                 # Folder for storing face images
├── dist/
│   └── FERRDY.exe        # Standalone executable
└── README.md             # This file
```

## 🛠️ Technology Stack

- **GUI Framework:** tkinter (Python built-in)
- **Face Recognition:** DeepFace with Facenet model
- **Speech Recognition:** Google Cloud Speech-to-Text API
- **Text-to-Speech:** pyttsx3
- **Computer Vision:** OpenCV
- **Deep Learning:** TensorFlow & Keras
- **Packaging:** PyInstaller

## 📦 Dependencies

```
opencv-python
deepface
numpy
speechrecognition
pyttsx3
pyaudio
tensorflow
```

## 🔧 How It Works

1. **Face Authentication** - Uses DeepFace to extract face embeddings and verify identity
2. **Voice Recognition** - Captures audio and converts to text using Google Speech API
3. **Command Processing** - Matches voice input to available commands
4. **Voice Response** - Uses pyttsx3 to synthesize and play audio response
5. **Command Execution** - Opens applications or performs requested actions
6. **History Logging** - Records all interactions in the GUI

## ⚙️ Settings Guide

### Test Mode
- Enables testing without face authentication
- Useful for development and voice command testing
- Can be toggled in the Settings tab

### Face Recognition Threshold
- **Lower value (0.3)** = Stricter matching, higher security
- **Higher value (1.0)** = Looser matching, easier to authenticate
- Default: 0.6

## 🐛 Troubleshooting

### GUI Won't Launch
- Ensure tkinter is available (included with Python)
- On Linux: `sudo apt-get install python3-tk`

### Microphone Not Detected
- Check Windows sound settings
- Ensure microphone is set as default input device
- Run the app with admin privileges if needed

### Face Authentication Fails
- Add clear, well-lit face photos to `faces/` folder
- Adjust threshold in Settings tab
- Use multiple photos with different angles

### No Audio Output
- Check speaker volume and connections
- Ensure speakers are set as default output device

### Google Speech API Errors
- Check internet connection
- Speak clearly and slowly
- Ensure minimal background noise

## 📝 Building from Source

To create your own FERRDY.exe:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller FERRDY.spec

# Find executable in dist/ folder
```


## 📝 Building from Source

To create your own FERRDY.exe:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller FERRDY.spec

# Find executable in dist/ folder
```

## 📄 License

MIT License - Feel free to use and modify!

## 👨‍💻 Author

Created by Sathya

## 💬 Support

For issues and feature requests, please open an issue on GitHub.

---

**Enjoy using FERRDY! 🎉**

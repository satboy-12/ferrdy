import speech_recognition as sr
import pyttsx3
import os
from datetime import datetime
import webbrowser

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

def speak(text):
    """Speak text using text-to-speech without printing to console"""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[ERROR] Could not play audio: {e}")

def listen():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    
    try:
        with sr.Microphone() as source:
            print("[LISTENING] Waiting for audio...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
    except sr.MicrophoneError as e:
        print(f"[ERROR] Microphone error: {e}")
        speak("Sorry, I cannot access the microphone")
        return ""
    except sr.RequestError as e:
        print(f"[ERROR] Internet connection error: {e}")
        speak("Please check your internet connection")
        return ""
    except Exception as e:
        print(f"[ERROR] Error accessing microphone: {e}")
        return ""

    try:
        command = r.recognize_google(audio)
        print(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("[ERROR] Could not understand audio")
        speak("Sorry, I did not catch that. Please speak again")
        return ""
    except sr.RequestError as e:
        print(f"[ERROR] Google API error: {e}")
        speak("Error with speech recognition service")
        return ""
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return ""

def process_command(cmd):
    """Process voice commands with expanded functionality"""
    
    if "open chrome" in cmd:
        os.system("start chrome")
        speak("Opening Chrome browser for you")
        return False

    elif "open vs code" in cmd or "open code" in cmd:
        os.system("code")
        speak("Opening Visual Studio Code")
        return False
    
    elif "open notepad" in cmd:
        os.system("start notepad")
        speak("Opening Notepad")
        return False

    elif "health" in cmd or "health tip" in cmd:
        tips = [
            "Remember to drink plenty of water throughout the day.",
            "Take a short break every hour to stretch your muscles.",
            "Get at least 7 hours of sleep for better health.",
            "Exercise regularly for a healthy lifestyle.",
            "Eat a balanced diet with fruits and vegetables."
        ]
        import random
        tip = random.choice(tips)
        speak(tip)
        return False
    
    elif "time" in cmd:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return False
    
    elif "date" in cmd:
        current_date = datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {current_date}")
        return False
    
    elif "search" in cmd:
        query = cmd.replace("search", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("Please specify what you want to search for")
        return False
    
    elif "tell me a joke" in cmd or "joke" in cmd:
        jokes = [
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that is a hardware problem!",
            "Why did the database break up with the spreadsheet? It wanted more structure!"
        ]
        import random
        joke = random.choice(jokes)
        speak(joke)
        return False
    
    elif "who are you" in cmd or "introduce" in cmd:
        speak("I am Ferrdy, your personal AI assistant. I can help you open applications, search the web, tell jokes, and much more!")
        return False
    
    elif "help" in cmd or "what can you do" in cmd:
        help_text = "I can open Chrome, Visual Studio Code, Notepad. Tell you the time and date. Search the internet. Tell jokes. Give health tips. And more!"
        speak(help_text)
        return False

    elif "exit" in cmd or "bye" in cmd or "goodbye" in cmd:
        speak("Goodbye buddy. Thanks for using Ferrdy!")
        return True

    else:
        speak("Sorry, I did not understand that command. Try saying help to hear what I can do.")
        return False

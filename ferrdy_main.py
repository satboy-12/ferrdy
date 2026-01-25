from face_auth import authenticate_face
from voice_assistant import speak, listen, process_command
import sys

# Check for test mode
test_mode = "--test" in sys.argv

if test_mode:
    print("[TEST MODE] Skipping face authentication")
    speak("Test mode activated. Listening for voice commands.")
else:
    if authenticate_face():
        speak("Welcome buddy. I am Ferrdy, your personal AI assistant.")
    else:
        print("Face authentication failed. Exiting.")
        exit()

print("[READY] Listening for commands...")
print("Available commands: open chrome, open vs code, health, exit")

try:
    while True:
        command = listen()
        if command:
            should_exit = process_command(command)
            if should_exit:
                break
except KeyboardInterrupt:
    print("\nShutting down FERRDY")
    speak("Goodbye")

print("[DONE] FERRDY shut down successfully")

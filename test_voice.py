import pyttsx3

print("Testing FERRDY Voice Output...")
print("=" * 50)

engine = pyttsx3.init()
engine.setProperty('rate', 175)  # Speed of speech

# Test 1: Simple greeting
print("\n[TEST 1] Playing greeting message...")
engine.say("Hello, I am Ferrdy, your personal AI assistant")
engine.runAndWait()

# Test 2: Confirmation
print("[TEST 2] Playing confirmation...")
engine.say("Voice output is working correctly")
engine.runAndWait()

# Test 3: Ready message
print("[TEST 3] Playing ready message...")
engine.say("I am ready to listen to your commands")
engine.runAndWait()

print("\n" + "=" * 50)
print("Voice test complete! If you heard audio, voice is working.")
print("If you didn't hear audio, check your speaker volume.")

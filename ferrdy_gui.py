import tkinter as tk
from tkinter import ttk, messagebox
import threading
from face_auth import authenticate_face
from voice_assistant import speak, listen, process_command
from datetime import datetime
import sys

class FERRDYApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FERRDY - AI Voice Assistant")
        self.root.geometry("700x850")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(True, True)
        
        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', background="#1e1e1e", foreground="#ffffff")
        self.style.configure('Title.TLabel', font=('Helvetica', 20, 'bold'), background="#1e1e1e", foreground="#00d4ff")
        self.style.configure('Status.TLabel', font=('Helvetica', 10), background="#1e1e1e", foreground="#00ff00")
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.map('TButton', background=[('active', '#00d4ff')])
        self.style.configure('Settings.TLabel', font=('Helvetica', 9), background="#1e1e1e", foreground="#cccccc")
        
        # State Variables
        self.authenticated = False
        self.listening = False
        self.command_history = []
        self.test_mode = False
        self.face_threshold = 0.6
        self.listening_indicator = False
        
        # Setup UI
        self.setup_ui()
        
        # Animation loop for listening indicator
        self.animate_listening()
        
    def setup_ui(self):
        """Setup the main UI components"""
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Main Tab
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="🏠 Home")
        self.setup_main_tab(main_frame)
        
        # Settings Tab
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        self.setup_settings_tab(settings_frame)
        
        # Help Tab
        help_frame = ttk.Frame(self.notebook)
        self.notebook.add(help_frame, text="ℹ️ Help")
        self.setup_help_tab(help_frame)
    
    def setup_main_tab(self, parent):
        """Setup main control tab"""
        
        # Top Frame - Title
        title_frame = ttk.Frame(parent)
        title_frame.pack(pady=15)
        
        title = ttk.Label(title_frame, text="🤖 FERRDY", style='Title.TLabel')
        title.pack()
        
        subtitle = ttk.Label(title_frame, text="AI Voice Assistant with Face Authentication", foreground="#888888")
        subtitle.pack()
        
        # Authentication Frame
        auth_frame = ttk.LabelFrame(parent, text="Authentication", padding=20)
        auth_frame.pack(padx=15, pady=10, fill="x")
        
        self.auth_status_label = ttk.Label(auth_frame, text="Status: Not Authenticated ❌", style='Status.TLabel', foreground="#ff6b6b")
        self.auth_status_label.pack(pady=10)
        
        auth_button_frame = ttk.Frame(auth_frame)
        auth_button_frame.pack(fill="x", pady=10)
        
        self.auth_button = ttk.Button(auth_button_frame, text="🔐 Authenticate Face", command=self.start_face_auth)
        self.auth_button.pack(side="left", padx=5, fill="x", expand=True)
        
        ttk.Button(auth_button_frame, text="🔄 Refresh", command=self.refresh_status).pack(side="left", padx=5)
        
        # Control Frame
        control_frame = ttk.LabelFrame(parent, text="Voice Control", padding=20)
        control_frame.pack(padx=15, pady=10, fill="x")
        
        self.listen_button = ttk.Button(control_frame, text="🎤 Listen for Commands", command=self.start_listening, state="disabled")
        self.listen_button.pack(pady=10, fill="x")
        
        # Visual Indicator
        indicator_frame = ttk.Frame(control_frame)
        indicator_frame.pack(pady=10)
        
        self.indicator_label = ttk.Label(indicator_frame, text="⚫ Ready", foreground="#888888")
        self.indicator_label.pack()
        
        self.command_label = ttk.Label(control_frame, text="Ready for commands...", foreground="#888888")
        self.command_label.pack(pady=5)
        
        # Quick Commands Frame
        quick_frame = ttk.LabelFrame(parent, text="Quick Commands", padding=15)
        quick_frame.pack(padx=15, pady=10, fill="x")
        
        button_grid = ttk.Frame(quick_frame)
        button_grid.pack(fill="x")
        
        ttk.Button(button_grid, text="Chrome", command=lambda: self.execute_command("open chrome")).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(button_grid, text="VS Code", command=lambda: self.execute_command("open vs code")).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(button_grid, text="Health", command=lambda: self.execute_command("health")).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ttk.Button(button_grid, text="Time", command=lambda: self.execute_command("time")).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(button_grid, text="Date", command=lambda: self.execute_command("date")).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(button_grid, text="Exit", command=self.shutdown_app).grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        for i in range(3):
            button_grid.grid_columnconfigure(i, weight=1)
        
        # History Frame
        history_frame = ttk.LabelFrame(parent, text="Command History", padding=15)
        history_frame.pack(padx=15, pady=10, fill="both", expand=True)
        
        # Scrollbar for history
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_text = tk.Text(history_frame, height=10, width=50, bg="#2d2d2d", fg="#00ff00", 
                                    yscrollcommand=scrollbar.set, font=('Courier', 9))
        self.history_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.history_text.yview)
        self.history_text.config(state="disabled")
    
    def setup_settings_tab(self, parent):
        """Setup settings tab"""
        
        settings_inner = ttk.Frame(parent, padding=20)
        settings_inner.pack(fill="both", expand=True)
        
        # Test Mode
        test_mode_frame = ttk.LabelFrame(settings_inner, text="Test Mode", padding=15)
        test_mode_frame.pack(fill="x", pady=10)
        
        ttk.Label(test_mode_frame, text="Skip face authentication for testing", style='Settings.TLabel').pack(anchor="w")
        
        self.test_mode_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(test_mode_frame, text="Enable Test Mode", variable=self.test_mode_var, command=self.toggle_test_mode).pack(anchor="w", pady=5)
        
        # Face Recognition Threshold
        threshold_frame = ttk.LabelFrame(settings_inner, text="Face Recognition Threshold", padding=15)
        threshold_frame.pack(fill="x", pady=10)
        
        ttk.Label(threshold_frame, text="Lower = Stricter (Default: 0.6)", style='Settings.TLabel').pack(anchor="w")
        
        threshold_subframe = ttk.Frame(threshold_frame)
        threshold_subframe.pack(fill="x", pady=10)
        
        ttk.Label(threshold_subframe, text="0.3", style='Settings.TLabel').pack(side="left")
        
        self.threshold_slider = ttk.Scale(threshold_subframe, from_=0.3, to=1.0, orient="horizontal", command=self.update_threshold)
        self.threshold_slider.set(0.6)
        self.threshold_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        self.threshold_label = ttk.Label(threshold_subframe, text="0.60", style='Settings.TLabel')
        self.threshold_label.pack(side="left")
        
        # Audio Settings
        audio_frame = ttk.LabelFrame(settings_inner, text="Audio Settings", padding=15)
        audio_frame.pack(fill="x", pady=10)
        
        ttk.Label(audio_frame, text="Microphone Sensitivity: High", style='Settings.TLabel').pack(anchor="w")
        ttk.Label(audio_frame, text="Speech Rate: 150 WPM", style='Settings.TLabel').pack(anchor="w")
        ttk.Label(audio_frame, text="Volume: 100%", style='Settings.TLabel').pack(anchor="w")
        
        # About
        about_frame = ttk.LabelFrame(settings_inner, text="About", padding=15)
        about_frame.pack(fill="x", pady=10)
        
        ttk.Label(about_frame, text="FERRDY v1.0", style='Settings.TLabel').pack(anchor="w")
        ttk.Label(about_frame, text="AI-powered Voice Assistant with Biometric Authentication", style='Settings.TLabel').pack(anchor="w")
        ttk.Label(about_frame, text="Built with: TensorFlow, DeepFace, SpeechRecognition", style='Settings.TLabel').pack(anchor="w")
    
    def setup_help_tab(self, parent):
        """Setup help tab"""
        
        help_inner = ttk.Frame(parent, padding=20)
        help_inner.pack(fill="both", expand=True)
        
        # Create text widget with scrollbar
        scrollbar = ttk.Scrollbar(help_inner)
        scrollbar.pack(side="right", fill="y")
        
        help_text = tk.Text(help_inner, height=30, bg="#2d2d2d", fg="#00ff00", 
                           yscrollcommand=scrollbar.set, font=('Courier', 9), wrap="word")
        help_text.pack(fill="both", expand=True)
        scrollbar.config(command=help_text.yview)
        
        help_content = """
=== FERRDY - AI Voice Assistant Help ===

[GETTING STARTED]
1. Click "Authenticate Face" to verify your identity
2. Once authenticated, use voice commands or quick buttons
3. Speak clearly when the app is listening

[VOICE COMMANDS]
- "open chrome"     : Launch Google Chrome
- "open vs code"    : Launch Visual Studio Code
- "open notepad"    : Launch Notepad
- "health"          : Get a health tip
- "time"            : Get current time
- "date"            : Get current date
- "search [query]"  : Search on Google
- "exit"            : Close the assistant

[FEATURES]
✓ Face Recognition Authentication
✓ Voice Command Processing
✓ Real-time Command History
✓ Quick Command Buttons
✓ Customizable Settings
✓ Test Mode for Development

[SETTINGS]
- Test Mode: Skip face auth for testing
- Threshold: Adjust face recognition strictness
- Lower threshold = stricter matching (more secure)

[TROUBLESHOOTING]
Problem: Microphone not working
→ Check Windows audio settings and permissions

Problem: Face not recognized
→ Ensure good lighting and clear face view
→ Adjust threshold in settings for stricter matching

Problem: Poor speech recognition
→ Speak clearly and slowly
→ Ensure minimal background noise

[KEYBOARD SHORTCUTS]
(Ctrl+Q to exit application when focused)

Need more help? Check the GitHub repository!
        """
        
        help_text.insert("1.0", help_content)
        help_text.config(state="disabled")
    
    def toggle_test_mode(self):
        """Toggle test mode"""
        self.test_mode = self.test_mode_var.get()
        if self.test_mode:
            self.auth_status_label.config(text="Status: Test Mode Enabled ⚠️", foreground="#ffb700")
            self.listen_button.config(state="normal")
            self.authenticated = True
            self.add_to_history("[SYSTEM] Test mode enabled - skipping face auth")
            speak("Test mode activated. Listening for voice commands.")
        else:
            self.auth_status_label.config(text="Status: Test Mode Disabled", foreground="#ff6b6b")
            self.authenticated = False
            self.listen_button.config(state="disabled")
            self.add_to_history("[SYSTEM] Test mode disabled")
    
    def update_threshold(self, value):
        """Update face recognition threshold"""
        self.face_threshold = float(value)
        self.threshold_label.config(text=f"{self.face_threshold:.2f}")
    
    def refresh_status(self):
        """Refresh authentication status"""
        if self.authenticated:
            self.add_to_history("[SYSTEM] Status check: Authenticated ✅")
        else:
            self.add_to_history("[SYSTEM] Status check: Not authenticated")
    
    def animate_listening(self):
        """Animate listening indicator"""
        if self.listening:
            if self.listening_indicator:
                self.indicator_label.config(text="🔴 Listening", foreground="#ff6b6b")
                self.listening_indicator = False
            else:
                self.indicator_label.config(text="🟢 Listening", foreground="#00ff00")
                self.listening_indicator = True
            self.root.after(500, self.animate_listening)
        else:
            self.indicator_label.config(text="⚫ Ready", foreground="#888888")
            self.root.after(100, self.animate_listening)
    
    def shutdown_app(self):
        """Shutdown the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit FERRDY?"):
            speak("Goodbye")
            self.root.quit()
    
    def start_face_auth(self):
        """Start face authentication in a separate thread"""
        if self.authenticated:
            messagebox.showinfo("Already Authenticated", "You are already authenticated!")
            return
        
        self.auth_button.config(state="disabled")
        self.auth_status_label.config(text="Status: Authenticating... ⏳", foreground="#ffb700")
        self.root.update()
        
        thread = threading.Thread(target=self._authenticate, daemon=True)
        thread.start()
    
    def _authenticate(self):
        """Authenticate face and update UI"""
        try:
            if authenticate_face(threshold=self.face_threshold):
                self.authenticated = True
                self.auth_status_label.config(text="Status: Authenticated ✅", foreground="#00ff00")
                self.listen_button.config(state="normal")
                speak("Welcome buddy. I am Ferrdy, your personal AI assistant.")
                self.add_to_history("[SYSTEM] Face authentication successful!")
            else:
                self.auth_status_label.config(text="Status: Authentication Failed ❌", foreground="#ff6b6b")
                self.add_to_history("[SYSTEM] Face authentication failed!")
        except Exception as e:
            self.auth_status_label.config(text=f"Status: Error ❌", foreground="#ff6b6b")
            self.add_to_history(f"[ERROR] {str(e)}")
        finally:
            self.auth_button.config(state="normal")
    
    def start_listening(self):
        """Start listening for voice commands in a separate thread"""
        if not self.authenticated:
            messagebox.showwarning("Not Authenticated", "Please authenticate first!")
            return
        
        self.listening = True
        self.listen_button.config(state="disabled")
        self.command_label.config(text="Listening... 🎤", foreground="#00d4ff")
        self.root.update()
        
        thread = threading.Thread(target=self._listen_and_process, daemon=True)
        thread.start()
    
    def _listen_and_process(self):
        """Listen and process voice commands"""
        try:
            command = listen()
            if command:
                self.command_label.config(text=f"Command: {command}", foreground="#00ff00")
                self.add_to_history(f"[YOU] {command}")
                
                self.root.after(500, lambda: self._execute_voice_command(command))
            else:
                self.command_label.config(text="No command detected", foreground="#888888")
        except Exception as e:
            self.command_label.config(text=f"Error: {str(e)}", foreground="#ff6b6b")
            self.add_to_history(f"[ERROR] {str(e)}")
        finally:
            self.listening = False
            self.listen_button.config(state="normal")
    
    def _execute_voice_command(self, command):
        """Execute the voice command"""
        should_exit = process_command(command)
        self.add_to_history(f"[FERRDY] Processing: {command}")
        
        if should_exit:
            self.shutdown_app()
    
    def execute_command(self, command):
        """Execute quick command"""
        if not self.authenticated:
            messagebox.showwarning("Not Authenticated", "Please authenticate first!")
            return
        
        self.add_to_history(f"[QUICK] {command}")
        thread = threading.Thread(target=lambda: process_command(command), daemon=True)
        thread.start()
    
    def add_to_history(self, message):
        """Add message to command history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {message}\n"
        
        self.history_text.config(state="normal")
        self.history_text.insert("end", history_entry)
        self.history_text.see("end")
        self.history_text.config(state="disabled")
        
        self.command_history.append(history_entry)

def main():
    root = tk.Tk()
    app = FERRDYApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

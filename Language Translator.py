import pyttsx3
from tkinter import Tk, Label, Text, Button, END, ttk, StringVar
from tkinter import PhotoImage
from deep_translator import GoogleTranslator
import speech_recognition as sr

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak_text(text):
    """Speak the given text using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def translate_text():
    """Translate the entered text and display the result."""
    source_text = source_text_area.get("1.0", END).strip()
    target_language = target_language_combobox.get()

    if not source_text:
        result_label.config(text="Please enter text to translate.")
        return

    if not target_language:
        result_label.config(text="Please select a target language.")
        return

    try:
        # Translate the text
        translated_text = GoogleTranslator(source="auto", target=target_language).translate(source_text)
        result_label.config(text="Translation Successful!", fg="green")
        translated_text_area.delete("1.0", END)
        translated_text_area.insert(END, translated_text)
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

def listen_and_transcribe():
    """Listen to the user's voice and transcribe it into the source text area."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        result_label.config(text="Listening... Please speak.", fg="blue")
        try:
            audio = recognizer.listen(source, timeout=5)
            transcribed_text = recognizer.recognize_google(audio)
            source_text_area.delete("1.0", END)
            source_text_area.insert(END, transcribed_text)
            result_label.config(text="Speech-to-text completed!", fg="green")
        except sr.UnknownValueError:
            result_label.config(text="Could not understand the audio.", fg="red")
        except sr.RequestError:
            result_label.config(text="Speech Recognition service is unavailable.", fg="red")
        except Exception as e:
            result_label.config(text=f"Error: {e}", fg="red")

def speak_translated_text():
    """Speak the translated text."""
    translated_text = translated_text_area.get("1.0", END).strip()
    if translated_text:
        speak_text(translated_text)
    else:
        result_label.config(text="No translation to speak.", fg="red")

def toggle_theme():
    """Toggle between light and dark mode."""
    current_theme = theme_var.get()
    if current_theme == "Light":
        app.configure(bg="white")
        title_label.config(bg="white", fg="black")
        result_label.config(bg="white", fg="black")
        for widget in [source_text_area, translated_text_area]:
            widget.config(bg="white", fg="black", insertbackground="black")
        theme_toggle_button.config(text="Switch to Dark Mode")
        theme_var.set("Dark")
    else:
        app.configure(bg="black")
        title_label.config(bg="black", fg="white")
        result_label.config(bg="black", fg="white")
        for widget in [source_text_area, translated_text_area]:
            widget.config(bg="black", fg="white", insertbackground="white")
        theme_toggle_button.config(text="Switch to Light Mode")
        theme_var.set("Light")

# Initialize Tkinter Window
app = Tk()
app.title("Language Translator with Audio Features")
app.geometry("600x500")
app.resizable(False, False)
app.configure(bg="white")

# Initialize theme variable
theme_var = StringVar(value="Light")

# Title
title_label = Label(app, text="Language Translator with Audio", font=("Arial", 16, "bold"), bg="white", fg="black")
title_label.pack(pady=10)

# Source Text Area
Label(app, text="Enter text to translate (or use mic):", font=("Arial", 12), bg="white", fg="black").pack(anchor="w", padx=10)
source_text_area = Text(app, height=5, width=70, bg="white", fg="black", insertbackground="black")
source_text_area.pack(pady=5)

# Mic Button
mic_button = Button(app, text="🎤 Speak", font=("Arial", 12), command=listen_and_transcribe)
mic_button.pack(pady=5)

# Target Language Selection
Label(app, text="Select Target Language:", font=("Arial", 12), bg="white", fg="black").pack(anchor="w", padx=10)
target_language_combobox = ttk.Combobox(app, values=GoogleTranslator().get_supported_languages(), width=30)
target_language_combobox.pack(pady=5)

# Translate Button
translate_button = Button(app, text="Translate", font=("Arial", 12), command=translate_text)
translate_button.pack(pady=10)

# Result Label
result_label = Label(app, text="", font=("Arial", 10), bg="white", fg="black")
result_label.pack()

# Translated Text Area
Label(app, text="Translated text (listen below):", font=("Arial", 12), bg="white", fg="black").pack(anchor="w", padx=10)
translated_text_area = Text(app, height=5, width=70, bg="white", fg="black", insertbackground="black")
translated_text_area.pack(pady=5)

# Speak Button for Translated Text
speak_button = Button(app, text="🔊 Speak Translation", font=("Arial", 12), command=speak_translated_text)
speak_button.pack(pady=5)

# Theme Toggle Button
theme_toggle_button = Button(app, text="Switch to Dark Mode", font=("Arial", 12), command=toggle_theme)
theme_toggle_button.pack(pady=5)

# Run the App
app.mainloop()

import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
import pyttsx3
import replicate.client
import requests
import replicate
import speech_recognition as sr
import threading
import musicLibrary

from langdetect import detect
from gtts import gTTS
import pygame
import os
import uuid
from deep_translator import GoogleTranslator
from threading import Lock
import customtkinter as ctk
from dotenv import load_dotenv   

# Load environment variables from .env file
load_dotenv()

# Initialize TTS
engine = pyttsx3.init()

#  API Keys (read from environment instead of hardcoding)
newsapi = os.getenv("NEWS_API_KEY")
replicate_token = os.getenv("REPLICATE_API_TOKEN")
groq_key = os.getenv("GROQ_API_KEY")

def translate_to(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return text

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

speak_lock = Lock()

def speak(text, lang='en'):
    with speak_lock:
        try:
            if lang == 'ur':
                filename = f"output_{uuid.uuid4()}.mp3"
                tts = gTTS(text=text, lang='ur')
                tts.save(filename)

                pygame.mixer.init()
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.quit()
                os.remove(filename)

            else:
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                engine.setProperty('rate', 160)
                engine.say(text)
                engine.runAndWait()
        except Exception as e:
            print(f"Speak error: {e}")

def log_output(text, lang="en"):
    output_area.insert(tk.END, text + "\n")
    output_area.see(tk.END)
    speak(text, lang=lang)

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {groq_key}",  # <-- uses env var
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful voice assistant named Jarvis."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            log_output(f"Groq API Error {response.status_code}: {response.text}")
            return "Sorry, I couldn't process that right now."
    except Exception as e:
        log_output("Error: " + str(e))
        return "Error: " + str(e)

def generate_image(prompt):
    log_output("Jarvis: Generating image...")
    try:
        client = replicate.Client(api_token=replicate_token)  # <-- uses env var
        output = client.run("stability-ai/sdxl", input={"prompt": prompt})
        image_url = output[0]
        webbrowser.open(image_url)
        log_output(f"Image generated: {image_url}")
    except Exception as e:
        log_output("Error generating image: " + str(e))

def process_command(c):
    user_lang = detect_language(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")  # <-- env var
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:
                log_output(article['title'])
        else:
            log_output("Failed to fetch news.")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "generate image" in c.lower() or "draw" in c.lower():
        prompt = c.lower().replace("generate image of", "").replace("draw", "").strip()
        generate_image(prompt)
    else:
        response = ask_groq(c)
        if not response:
            log_output("Jarvis: No response received from Groq.")
        else:
            if user_lang == "ur":
                response = translate_to(response, "ur")
                log_output("Jarvis: " + response, lang=user_lang)
            else:
                log_output("Jarvis: " + response)

def voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        log_output("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            log_output("You: " + command)
            process_command(command)
        except Exception as e:
            import traceback
            log_output("Voice command error: " + str(e))
            traceback.print_exc()

def start_voice_thread():
    threading.Thread(target=voice_command).start()

def run_text_command():
    text = text_entry.get()
    if text.strip():
        log_output("You: " + text)
        threading.Thread(target=process_command, args=(text,)).start()
    text_entry.delete(0, tk.END)

# GUI Setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🧠 Jarvis Desktop AI")
app.geometry("1000x700")
app.state("zoomed")

title = ctk.CTkLabel(app, text="🧠 Jarvis AI Assistant", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=20)

output_area = ctk.CTkTextbox(app, height=500, font=("Segoe UI", 14), wrap="word")
output_area.pack(padx=20, pady=10, fill="both", expand=True)

input_frame = ctk.CTkFrame(app, fg_color="#f1f1f1", corner_radius=20)
input_frame.pack(pady=15, padx=20, fill="x", side="bottom")

text_entry = ctk.CTkEntry(
    input_frame,
    height=45,
    font=("Segoe UI", 13),
    placeholder_text="Message Jarvis..."
)
text_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

voice_button = ctk.CTkButton(
    input_frame, text="🎤", width=45, height=45,
    fg_color="#00c67c", text_color="white",
    font=ctk.CTkFont(size=16, weight="bold"),
    corner_radius=12, command=start_voice_thread
)
voice_button.pack(side="left", padx=5, pady=10)

text_button = ctk.CTkButton(
    input_frame, text="➤", width=45, height=45,
    fg_color="#0a84ff", text_color="white",
    font=ctk.CTkFont(size=16, weight="bold"),
    corner_radius=12, command=run_text_command
)
text_button.pack(side="left", padx=(5, 10), pady=10)

app.mainloop()










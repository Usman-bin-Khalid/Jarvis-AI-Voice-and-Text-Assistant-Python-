# 🧠 Jarvis AI Voice & Text Assistant  

Jarvis is a **powerful AI desktop assistant** built in **Python** with **voice & text command support**.  
It can talk, translate, generate images, fetch news, play songs, open websites, and interact using **Groq LLM + Replicate AI**.  
With a modern **Tkinter (CustomTkinter) GUI**, Jarvis is your personal AI companion for everyday tasks.  

---

## ✨ Features  
- 🎤 **Voice Commands** (using SpeechRecognition + Google API)  
- ⌨️ **Text Commands** with real-time responses  
- 🌍 **Multi-language Support** (auto language detection + Urdu translation)  
- 🗞️ **Live News Fetching** (via NewsAPI)  
- 🎶 **Music Playback** (custom music library)  
- 🖼️ **AI Image Generation** (via Replicate API - Stability AI)  
- 🔗 **Smart Web Access** (Google, YouTube, custom sites)  
- 🗣️ **Dual TTS Engine**:  
  - English → Pyttsx3 (male voice)  
  - Urdu → gTTS + Pygame  
- 🖥️ **Modern UI** with CustomTkinter (chat-style interface)  

---

## 🚀 Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/Usman-bin-Khalid/Jarvis-AI-Voice-and-Text-Assistant-Python-.git
   cd Jarvis-AI-Assistant
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Add your API Keys in the script:

newsapi → News API

replicate_token → Replicate

groq_api_key → Groq API

Run the app:

bash
Copy code
python main.py
⚙️ Requirements
Python 3.9+

tkinter, customtkinter, pyttsx3, pygame, gTTS, speechrecognition, replicate, requests, langdetect, deep-translator

Install with:

bash
Copy code
pip install pyttsx3 pygame gTTS SpeechRecognition replicate requests langdetect deep-translator customtkinter
📜 License
This project is Open Source under the MIT License.

🙌 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to fork this repo and submit a PR.

🌟 Acknowledgments
Groq API

Replicate

NewsAPI

CustomTkinter


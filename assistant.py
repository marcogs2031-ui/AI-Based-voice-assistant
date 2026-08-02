# Part 1: Library Imports & PyAudio Patch
import pyaudiowpatch as pyaudio
import sys
sys.modules['pyaudio'] = pyaudio  # Engaña a speech_recognition para que use pyaudiowpatch

import speech_recognition as sr
import pyttsx3
import ollama

# Part 2: Voice Engine Initialization
engine = pyttsx3.init()

# Part 3: Text-to-Speech Function
def speak(text):
    print(f"\nAssistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Part 4: Dynamic Microphone Listener
def listen_microphone():
    recognizer = sr.Recognizer()
    
    # Silence detection setup
    recognizer.pause_threshold = 1.0 
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("\nListening (EN / ES / KO)... Speak whenever you are ready!")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)

    try:
        user_input = recognizer.recognize_google(audio, language="es-ES")
        print(f"You said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        speak("I couldn't understand the audio.")
    except Exception as e:
        print(f"Error: {e}")
        
    return ""

# Part 5: Stateless LLM Query (Ollama)
def query_ollama(prompt):
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {
                'role': 'system', 
                'content': (
                    'You are IVI, an intelligent multilingual voice assistant. '
                    'You can understand and speak English, Spanish, and Korean (한국어). '
                    'Always reply in the exact same language that the user uses to speak to you. '
                    'Keep your answers clear and concise.'
                )
            },
            {
                'role': 'user', 
                'content': prompt
            }
        ]
    )
    return response['message']['content']

# Part 6: Main Execution Loop
if __name__ == "__main__":
    speak("System online. IVI model is ready for English, Spanish, and Korean.")
    
    while True:
        command = listen_microphone()
        
        if command:
            if any(word in command.lower() for word in ["exit", "bye", "adios", "안녕"]):
                speak("Goodbye / ¡Hasta luego!")
                break
                
            speak("Processing...")
            response = query_ollama(command)
            speak(response)
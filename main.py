import pyttsx3
import speech_recognition as sr
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"Bot: {text}")
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Google Speech Recognition is not working right now.")
        return ""

def send_to_flask_chatbot(message):
    url = "http://127.0.0.1:5001/get"
    response = requests.post(url, json={"message": message})
    return response.json()["response"]

if __name__ == '__main__':
    speak("Hello, I am Ritik AI. How can I help you today?")

    while True:
        query = takeCommand()

        if query in ["exit", "stop", "quit"]:
            speak("Goodbye sir.")
            break

        if query:
            bot_reply = send_to_flask_chatbot(query)
            speak(bot_reply)

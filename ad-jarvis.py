import openai
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# === CONFIGURATION ===
openai.api_key = "sk-Your_API_Key"  # Replace with your OpenAI API key
FILE_DIRECTORY = r"C:\JarvisFiles"  # Folder containing local files you want to open

# === INITIALIZE JARVIS ===
jarvis = pyttsx3.init()
jarvis.setProperty('rate', 150)

def speak(text):
    print("Jarvis:", text)
    jarvis.say(text)
    jarvis.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Internet issue.")
        return ""

def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error communicating with ChatGPT: {e}"

def open_file_by_name(spoken_name):
    for file in os.listdir(FILE_DIRECTORY):
        filename = os.path.splitext(file)[0].lower()
        if filename in spoken_name:
            file_path = os.path.join(FILE_DIRECTORY, file)
            os.startfile(file_path)
            speak(f"Opening {file}")
            return True
    speak("Sorry, I couldn't find that file.")
    return False

def handle_command(command):
    if 'open youtube' in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif 'open facebook' in command:
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook.")
    elif 'open instagram' in command:
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram.")
    elif 'open chatgpt' in command or 'open cgpt' in command:
        webbrowser.open("https://chat.openai.com")
        speak("Opening ChatGPT.")
    elif 'time' in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif 'open file' in command:
        filename = command.replace('open file', '').strip()
        if filename:
            opened = open_file_by_name(filename)
            if not opened:
                speak("Trying to understand your request.")
                response = ask_chatgpt(command)
                speak(response)
        else:
            speak("Please say the name of the file to open.")
    elif 'shutdown' in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif 'exit' in command or 'bye' in command:
        speak("Goodbye! Jarvis signing off.")
        exit()
    else:
        # Anything else goes to ChatGPT
        response = ask_chatgpt(command)
        speak(response)

# === MAIN LOOP ===
speak("Jarvis is online with ChatGPT intelligence. How can I help you?")
while True:
    user_command = listen()
    if user_command:
        handle_command(user_command)

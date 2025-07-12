import openai
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# === CONFIG ===
openai.api_key = "sk-Your_API_Key"
FILE_DIRECTORY = r"C:\JarvisFiles"  # Folder containing files

# === SETUP ===
jarvis = pyttsx3.init()
jarvis.setProperty('rate', 150)
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    print("Jarvis:", text)
    jarvis.say(text)
    jarvis.runAndWait()

def listen_for_wake_word():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("👂 Waiting for 'Hey Jarvis'...")
        audio = recognizer.listen(source)
    try:
        phrase = recognizer.recognize_google(audio).lower()
        print("Heard:", phrase)
        return "hey jarvis" in phrase
    except:
        return False

def listen_command():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening for command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You:", command)
        return command
    except:
        speak("Sorry, I didn't catch that.")
        return ""

def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"ChatGPT error: {e}"

def open_file_by_name(spoken_name):
    for file in os.listdir(FILE_DIRECTORY):
        filename = os.path.splitext(file)[0].lower()
        if filename in spoken_name:
            os.startfile(os.path.join(FILE_DIRECTORY, file))
            speak(f"Opening {file}")
            return True
    speak("I couldn't find that file.")
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
            open_file_by_name(filename)
        else:
            speak("Please say the file name.")
    elif 'shutdown' in command:
        speak("Shutting down.")
        os.system("shutdown /s /t 1")
    elif 'exit' in command or 'bye' in command:
        speak("Goodbye.")
        exit()
    else:
        response = ask_chatgpt(command)
        speak(response)

# === MAIN LOOP ===
speak("Jarvis is now on standby. Say 'Hey Jarvis' to activate.")

while True:
    if listen_for_wake_word():
        speak("Yes, how can I help?")
        user_command = listen_command()
        if user_command:
            handle_command(user_command)

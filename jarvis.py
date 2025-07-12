import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# Set the path to the folder where your files are stored
FILE_DIRECTORY = r"C:\JarvisFiles"  # Change this path to your folder

# Initialize Jarvis
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
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Internet issue.")
        return ""

def open_file_by_name(spoken_name):
    # Normalize the spoken name (e.g., "my file" to "my file.pdf" or "my file.txt")
    for file in os.listdir(FILE_DIRECTORY):
        filename = os.path.splitext(file)[0].lower()  # Get file name without extension
        if filename in spoken_name:
            file_path = os.path.join(FILE_DIRECTORY, file)
            os.startfile(file_path)
            speak(f"Opening {file}")
            return
    speak("Sorry, I couldn't find that file.")

def respond(command):
    if 'hello' in command:
        speak("Hello, I am Jarvis. How can I help?")
    elif 'time' in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif 'open youtube' in command:
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
    elif 'open file' in command:
        filename = command.replace('open file', '').strip()
        if filename:
            open_file_by_name(filename)
        else:
            speak("Please say the name of the file to open.")
    elif 'shutdown' in command:
        speak("Shutting down your system.")
        os.system("shutdown /s /t 1")
    elif 'exit' in command or 'bye' in command:
        speak("Goodbye! Jarvis signing off.")
        exit()
    else:
        speak("I'm not sure how to help with that.")

# Start Jarvis
speak("Jarvis online. Ready to serve you.")
while True:
    command = listen()
    respond(command)

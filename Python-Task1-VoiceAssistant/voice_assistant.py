import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import sounddevice as sd
import wave
import tempfile
import os
from typing import Any, cast


# ==========================================
# SETTINGS
# ==========================================

# Tumhare system ka microphone
MICROPHONE_DEVICE = 1

# Recording settings
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 8


# ==========================================
# TEXT TO SPEECH
# ==========================================

engine = pyttsx3.init()

engine.setProperty("rate", 170)


def speak(text):
    print("Assistant:", text)

    engine.say(text)
    engine.runAndWait()


# ==========================================
# RECORD AUDIO
# ==========================================

def record_audio(filename):

    print("\n🎤 Listening...")
    print("Please speak now...")

    try:

        audio = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            device=MICROPHONE_DEVICE
        )

        sd.wait()

        with wave.open(filename, "wb") as audio_file:

            audio_file.setnchannels(CHANNELS)
            audio_file.setsampwidth(2)
            audio_file.setframerate(SAMPLE_RATE)

            audio_file.writeframes(
                audio.tobytes()
            )

        print("✅ Recording completed.")

        return True

    except Exception as error:

        print("Microphone Error:", error)

        return False


# ==========================================
# LISTEN
# ==========================================

def listen():

    recognizer = sr.Recognizer()

    # Speech recognition sensitivity
    recognizer.energy_threshold = 250
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    filename = temp_file.name

    temp_file.close()

    try:

        success = record_audio(filename)

        if not success:

            speak(
                "I could not access the microphone."
            )

            return ""

        print("🔄 Recognizing...")

        with sr.AudioFile(filename) as source:

            audio = recognizer.record(source)

        # Indian English
        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You:", command)

        return command.lower()

    except sr.UnknownValueError:

        speak(
            "Sorry, I could not understand you. "
            "Please speak clearly and try again."
        )

        return ""

    except sr.RequestError:

        speak(
            "Speech recognition service is unavailable. "
            "Please check your internet connection."
        )

        return ""

    except Exception as error:

        print("Recognition Error:", error)

        speak(
            "Something went wrong. Please try again."
        )

        return ""

    finally:

        if os.path.exists(filename):

            os.remove(filename)


# ==========================================
# TIME
# ==========================================

def tell_time():

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(
        f"The current time is {current_time}"
    )


# ==========================================
# DATE
# ==========================================

def tell_date():

    current_date = datetime.datetime.now().strftime(
        "%d %B %Y"
    )

    speak(
        f"Today's date is {current_date}"
    )


# ==========================================
# WEB SEARCH
# ==========================================

def web_search(command):

    search_query = command.replace(
        "search",
        "",
        1
    ).strip()

    if search_query:

        speak(
            f"Searching for {search_query}"
        )

        url = (
            "https://www.google.com/search?q="
            + search_query.replace(" ", "+")
        )

        webbrowser.open(url)

    else:

        speak(
            "What would you like me to search for?"
        )


# ==========================================
# MAIN ASSISTANT
# ==========================================

def run_assistant():

    speak(
        "Hello! I am your Python voice assistant. "
        "How can I help you?"
    )

    while True:

        command = listen()

        if command == "":
            continue

        # ------------------------------
        # HELLO
        # ------------------------------

        if (
            "hello" in command
            or "hi" in command
            or "hey" in command
        ):

            speak(
                "Hello! Nice to meet you. "
                "How can I help you?"
            )

        # ------------------------------
        # TIME
        # ------------------------------

        elif "time" in command:

            tell_time()

        # ------------------------------
        # DATE
        # ------------------------------

        elif (
            "date" in command
            or "today" in command
        ):

            tell_date()

        # ------------------------------
        # SEARCH
        # ------------------------------

        elif "search" in command:

            web_search(command)

        # ------------------------------
        # EXIT
        # ------------------------------

        elif (
            "exit" in command
            or "quit" in command
            or "stop" in command
            or "bye" in command
            or "goodbye" in command
        ):

            speak(
                "Goodbye! Have a nice day."
            )

            break

        # ------------------------------
        # UNKNOWN COMMAND
        # ------------------------------

        else:

            speak(
                "I don't understand that command yet."
            )


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":

    run_assistant()
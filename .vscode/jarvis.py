import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import datetime
import os
import time
import re
# =========================================================
# JARVIS VOICE ENGINE
# =========================================================
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()
# =========================================================
# SPEECH RECOGNITION
# ========================================================
recognizer = sr.Recognizer()
def listen():
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )
        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )
            print("🔄 Recognizing...")
            command = recognizer.recognize_google(
                audio,
                language="en-IN"
            )
            print("YOU:", command)
            return command.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("Could not understand.")
            return ""
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""
# =========================================================
# ADB FUNCTION
# =========================================================
def adb(command):
    try:
        result = subprocess.run(
            ["adb"] + command,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        speak("ADB is not installed or not added to PATH.")
        return ""
# =========================================================
# CHECK PHONE
# =========================================================
def check_phone():
    result = adb(["devices"])
    if "device" in result:
        print("📱 Android phone connected.")
        return True
    else:
        print("❌ Android phone not connected.")
        return False
# =========================================================
# OPEN ANDROID APP
# =========================================================
def open_app(package_name):
    speak("Opening application.")
    adb([
        "shell",
        "monkey",
        "-p",
        package_name,
        "1"
    ])
# =========================================================
# PHONE CALL
# =========================================================
def call_number(number):
    speak("Calling now.")
    adb([
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.CALL",
        "-d",
        f"tel:{number}"
    ])
# =========================================================
# OPEN DIALER
# =========================================================
def open_dialer():
    adb([
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.DIAL"
    ])
# ========================================================
# VOLUME UP
# =========================================================
def volume_up():
    adb([
        "shell",
        "input",
        "keyevent",
        "24"
    ])
# =========================================================
# VOLUME DOWN
# =========================================================
def volume_down():
    adb([
        "shell",
        "input",
        "keyevent",
        "25"
    ])
# =========================================================
# HOME BUTTON
# =========================================================
def home():
    adb([
        "shell",
        "input",
        "keyevent",
        "3"
    ])
# =========================================================
# BACK BUTTON
# =========================================================
def back():
    adb([
        "shell",
        "input",
        "keyevent",
        "4"
    ])
# =========================================================
# SCREENSHOT
# =========================================================
def screenshot():
    filename = "phone_screenshot.png"
    adb([
        "exec-out",
        "screencap",
        "-p"
    ])
    subprocess.run(
        f"adb exec-out screencap -p > {filename}",
        shell=True
    )
    speak("Screenshot captured.")
# =========================================================
# OPEN WEBSITE ON LAPTOP
# =========================================================
def open_website(url):
    webbrowser.open(url)
# =========================================================
# SYSTEM INFORMATION
# =========================================================
def current_time():
    current = datetime.datetime.now().strftime(
        "%I:%M %p"
    )
    speak(f"The time is {current}")
# =========================================================
# APP COMMANDS
# =========================================================
def handle_app(command):
    apps = {
        "youtube":
            "com.google.android.youtube",
        "whatsapp":
            "com.whatsapp",
        "instagram":
            "com.instagram.android",
        "telegram":
            "org.telegram.messenger",
        "chrome":
            "com.android.chrome",
        # Package may differ depending on
        # Android/JioHotstar version.
        "jio hotstar":
            "com.jiohotstar.app"
    }
    for app in apps:
        if app in command:
            open_app(apps[app])
            return True
    return False
# =========================================================
# COMMAND PROCESSOR
# =========================================================
def process_command(command):
    if not command:
        return True
    # -----------------------------------------
    # GREETING
    # -----------------------------------------
    if "hello jarvis" in command:
        speak("Hello sir. How can I help you?")
        return True
    # ----------------------------------------
    # TIME
    # -----------------------------------------
    if "time" in command:
        current_time()
        return True
    # -----------------------------------------
    # OPEN YOUTUBE
    # -----------------------------------------
    if "open youtube" in command:
        open_app(
            "com.google.android.youtube"
        )
        speak("YouTube opened.")
        return True
    # -----------------------------------------
    # OPEN WHATSAPP
    # -----------------------------------------
    if "open whatsapp" in command:
        open_app(
            "com.whatsapp"
        )
        speak("WhatsApp opened.")
        return True
    # -----------------------------------------
    # OPEN INSTAGRAM
    # -----------------------------------------
    if "open instagram" in command:
        open_app(
            "com.instagram.android"
        )
        speak("Instagram opened.")
        return True
    # -----------------------------------------
    # OPEN JIO HOTSTAR
    # -----------------------------------------
    if (
        "open jio hotstar" in command
        or
        "open hotstar" in command
    ):
        open_app(
            "com.jiohotstar.app"
        )
        speak("Jio Hotstar opened.")
        return True
    # -----------------------------------------
    # DIALER
    # -----------------------------------------
    if "open dialer" in command:

        open_dialer()
        return True
    # -----------------------------------------
    # CALL NUMBER
    # -----------------------------------------
    if "call" in command:
        numbers = re.findall(
            r"\+?\d[\d\s-]{8,}\d",
            command
        )
        if numbers:
            number = (
                numbers[0]
                .replace(" ", "")
                .replace("-", "")
            )
            call_number(number)
            return True
    # -----------------------------------------
    # VOLUME UP
    #-----------------------------------------
    if (
        "volume up" in command
        or
        "increase volume" in command
    ):
        volume_up()
        speak("Volume increased.")
        return True
    # -----------------------------------------
    # VOLUME DOWN
    # -----------------------------------------
    if (
        "volume down" in command
        or
        "decrease volume" in command
    ):
        volume_down()
        speak("Volume decreased.")
        return True
    # -----------------------------------------
    # HOME
    # -----------------------------------------
    if (
        "go home" in command
        or
        "home screen" in command
    ):
        home()
        return True
    # -----------------------------------------
    # BACK
    # -----------------------------------------
    if "go back" in command:
        back()
        return True
    # -----------------------------------------
    # SCREENSHOT
    # -----------------------------------------
    if "take screenshot" in command:
        screenshot()
        return True
    # -----------------------------------------
    # GOOGLE SEARCH
    # -----------------------------------------
    if "search google for" in command:
        query = command.replace(
            "search google for",
            ""
        ).strip()
        url = (
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )
        open_website(url)
        speak("Searching Google.")
        return True
    # -----------------------------------------
    # STOP
    # -----------------------------------------
    if (
        "exit" in command
        or
        "quit" in command
        or
        "shutdown jarvis" in command
    ):
        speak("Goodbye sir.")
        return False
    # -----------------------------------------
    # UNKNOWN COMMAND
    # -----------------------------------------
    speak(
        "I don't know how to perform that command yet."
    )
    return True
# =========================================================
# MAIN JARVIS LOOP
# =========================================================
def main():
    print("=" * 50)
    print("       J.A.R.V.I.S")
    print(" Android Voice Assistant")
    print("=" * 50)
    if check_phone():
        speak(
            "Android device connected. "
            "Jarvis is online."
        )
    else:
        speak(
            "No Android device detected."
        )
    while True:
        command = listen()
        if not process_command(command):
            break
# =========================================================
# START PROGRAM
# =========================================================
if __name__ == "__main__":
    main()
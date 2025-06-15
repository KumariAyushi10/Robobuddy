import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import pywhatkit
import time
import pygame
import pyjokes

# Initialize voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print(f"Robobuddy: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Robobuddy. How may I assist you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
    except Exception:
        speak("I didn't catch that. Could you please repeat?")
        return "None"
    return query.lower()

def getWeather():
    speak("Please say the name of the city.")
    city = takeCommand()
    if city == "none":
        return
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    try:
        geo_response = requests.get(geo_url).json()
        if "results" in geo_response:
            lat = geo_response["results"][0]["latitude"]
            lon = geo_response["results"][0]["longitude"]
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url).json()
            temp = weather_response["current_weather"]["temperature"]
            wind = weather_response["current_weather"]["windspeed"]
            speak(f"The temperature in {city} is {temp}°C with wind speed of {wind} km/h.")
        else:
            speak("City not found.")
    except:
        speak("Could not fetch weather. Please try again later.")

def playAlarm():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("alarm_sound.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def setAlarm():
    speak("Please tell the alarm time in 24 hour format like 14:30")
    alarm_time = takeCommand()
    if alarm_time == "none":
        return
    speak(f"Alarm set for {alarm_time}")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("It's time! Your alarm is ringing.")
            playAlarm()
            break
        time.sleep(30)

def sendEmail():
    try:
        speak("Enter your email ID:")
        email_id = input("Your Email: ")
        speak("Enter your password:")
        password = input("Password: ")
        speak("Enter the receiver's email:")
        to = input("Receiver's Email: ")
        speak("What should I say?")
        content = takeCommand()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_id, password)
        server.sendmail(email_id, to, content)
        server.quit()
        speak("Email has been sent successfully.")
    except:
        speak("Sorry. I couldn't send the email.")

def searchNearby(place):
    speak(f"Showing nearby {place} on Google Maps.")
    webbrowser.open(f"https://www.google.com/maps/search/{place}+near+me/")

def openApp(app_name):
    app_paths = {
        "spotify": "C:\\Users\\<your-username>\\AppData\\Roaming\\Spotify\\Spotify.exe",
        "netflix": "https://www.netflix.com",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "code": "C:\\Users\\<your-username>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
        "notepad": "notepad"
    }
    if app_name in app_paths:
        try:
            if app_paths[app_name].startswith("http"):
                webbrowser.open(app_paths[app_name])
            else:
                os.startfile(app_paths[app_name])
            speak(f"Opening {app_name}")
        except:
            speak(f"Failed to open {app_name}")
    else:
        speak("Application path not set.")

# ---------- Main Assistant ----------
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except:
                speak("Couldn't find any results.")

        elif "youtube" in query:
            webbrowser.open("https://www.youtube.com")

        elif "google" in query:
            webbrowser.open("https://www.google.com")

        elif "stack overflow" in query:
            webbrowser.open("https://stackoverflow.com")

        elif "play song" in query or "play music" in query:
            speak("Which song would you like to hear?")
            song = takeCommand()
            pywhatkit.playonyt(song)

        elif "search" in query:
            speak("What should I search?")
            search = takeCommand()
            pywhatkit.search(search)

        elif "weather" in query:
            getWeather()

        elif "set alarm" in query:
            setAlarm()

        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {current_time}")

        elif "date" in query or "day" in query:
            today = datetime.datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today is {today}")

        elif "email" in query:
            sendEmail()

        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "nearby hospital" in query:
            searchNearby("hospitals")

        elif "nearby restaurant" in query:
            searchNearby("restaurants")

        elif "nearby atm" in query:
            searchNearby("atm")

        elif "open spotify" in query:
            openApp("spotify")

        elif "open netflix" in query:
            openApp("netflix")

        elif "open chrome" in query:
            openApp("chrome")

        elif "open code" in query:
            openApp("code")

        elif "open notepad" in query:
            openApp("notepad")

        elif "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye! Robobuddy signing off.")
            break

        else:
            speak("I'm not sure how to do that. Can you try again?")

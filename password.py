import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import os
import smtplib
import requests

from keyboard import press
from pyautogui import click
from keyboard import press_and_release
#from features import GoogleSearch
from keyboard import write
from time import sleep
import webbrowser as web

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        speak("i am sorry sir could you repeat that please")
        return "None"
    return query

def Pass(pass_in):
    password = "python"
    passss = str(password)
    if passss==str(pass_in):
        speak("Access Granted")
        import jarvis
    else:
        speak("Access Denied .")

if __name__ == "__main__" :
    speak("This Particular File Is Password Protected")
    speak("Kindly Provide The Password To Access .")
    passsss = input(": Enter The Password :")
    #passsss = takeCommand()
    Pass(passsss)



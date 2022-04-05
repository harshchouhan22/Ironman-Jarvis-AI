import wikipedia
import os
import webbrowser as web
import pyttsx3
import pywhatkit
import requests
from keyboard import press_and_release
from bs4 import BeautifulSoup
import pafy
import speech_recognition as sr
import socket

import pyttsx3
import speech_recognition as sr
import webbrowser
from pywikihow import search_wikihow
from bs4 import BeautifulSoup
import pywhatkit
import wikipedia
from googletrans import Translator
import os
import pyautogui
import psutil
from tkinter import Label
from tkinter import Entry
from tkinter import Button
import requests
from tkinter import Tk
from gtts import gTTS
from tkinter import StringVar
import PyPDF2
from pytube import YouTube
import datetime
from playsound import playsound
import keyboard
import pyjokes


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def DateConverter(query):
    Date = query.replace(" and ", "-")
    Date = Date.replace(" and ", "-")
    Date = Date.replace("and", "-")
    Date = Date.replace("and", "-")
    Date = Date.replace(" ", "")
    return str(Date)

def YouTubeSearch(term):
    result = "https://www.youtube.com/results?search_query=" + term
    web.open(result)
    speak("This  Is What i found for your search .")
    pywhatkit.playonyt(term)
    speak("This May Also Help You Sir .")


def My_Location():
    op = "https://www.google.com/maps/@23.1865901,77.4596203,47m/data=!3m1!1e3"
    speak("Your Home Location")
  #  web.open(op)
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    state = geo_d['city']
    country = geo_d['country']
    speak(f"Sir, You Are In {state, country} .")
    print(f"state = {state}  , country = {country}")

from pytube import YouTube
from pyautogui import click
from pyautogui import hotkey
import  pyperclip
from time import sleep
import pyperclip  # pip install pyperclip required

import pyautogui


from pytube import YouTube

def youtube_video_download():
    press_and_release('F6')
    sleep(1)
    pyautogui.hotkey('ctrl', 'c')  # for copying the selected url
    url = pyperclip.paste()
 #   print(url)
    youtube_video_url = f'{url}'
    try:
        yt_obj = YouTube(youtube_video_url)

        filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')

        # download the highest quality video
        print(f'{yt_obj.title} is downloading From Youtube')
        speak(f'{yt_obj.title} is downloading From Youtube')

        filters.get_highest_resolution().download('F:\\Python AI\\database\\youtube_downloads', filename=f'{yt_obj.title}.mp4')
        print('Video Downloaded Successfully')
    except Exception as e:
        print(e)

from pytube import Playlist
def download_youtube_playlist():
    try:
        press_and_release('F6')
        sleep(1)
        pyautogui.hotkey('ctrl', 'c')  # for copying the selected url
        url = pyperclip.paste()
        playlist = Playlist(f'{url}')
        playlist.download_all(download_path='F:\\Python AI\\database\\youtube_downloads')
    except Exception as e:
        print(e)

from pytube import YouTube
def youtube_audio():
    press_and_release('F6')
    sleep(1)
    pyautogui.hotkey('ctrl', 'c')  # for copying the selected url
    url = pyperclip.paste()
    youtube_video_url = f'{url}'
    try:
        print('Downloading Start')
        speak('Downloading start')
        yt_obj = YouTube(youtube_video_url)
        yt_obj.streams.get_audio_only().download(output_path='F:\\Python AI\\database\\youtube_music', filename=f'{yt_obj.title}.mp3')
        print('YouTube video audio downloaded successfully')
        speak('YouTube video audio downloaded successfully')
    except Exception as e:
        print(e)


def Temp(search):
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)

    data = BeautifulSoup(r.text, "html.parser")
    temperature = data.find("div", class_="BNeawe").text
    print(f"The {search} is {temperature} celsius")
    speak(f"The {search} is {temperature} celsius")


import socket

def ipAddress():
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    print('My IP Adrress is : ' + ipAddress)
    speak('My IP Adrress is : ' + ipAddress)

import moviepy.editor as mp
#zzzzzzzzzfrom jarvis import takeCommand

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 100  # minimum audio energy to consider for recording
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def videotomp3():
    speak('which video sir?')
    video = takeCommand()
    video = mp.VideoFileClip(f"{video}.mp4")
    video.audio.write_audiofile(r"output.mp3")
    speak('Converting video to mp3.')
    print('Converting video to mp3.')

def shutdown():
    speak('shutting down computer')
    os.system("shutdown now - h")

import PyPDF2
def pdfreader(pdf):

    book = open(f'{pdf}.pdf', 'rb')
    pdf_reader = PyPDF2.PdfFileReader(book)
    num_pages = pdf_reader.numPages
    
    play = pyttsx3.init()
    print('Playing the Audio  book')
    for num in range(0,num_pages):
        page = pdf_reader.getPage(num)
        data = page.extractText()
        play.say(data)
        play.runAndWait()


#from requests_html import HTMLSession
from urllib.request import urlopen

#def ask_google1(query):
#    query = input("What would you like to search: ")
 #   query = query.replace(" ", "+")
 #   query = f"https://www.google.com/search?q=" + query
  #  r = requests.get(query)
   # html_doc = r.text
    #soup = BeautifulSoup(html_doc, 'html.parser')
    #for s in soup.find_all(id="rhs_block"):
     #   print(s.text)


#ask_google1("donald trump")

def screenshot():
    speak("Ok Boss , What Should I Name That File ?")
    path = takeCommand()
    path1name = path + ".png"
    path1 = "F:\\Python AI\\database\\Screenshots\\" + path1name
    kk = pyautogui.screenshot()
    kk.save(path1)
    os.startfile("F:\\Python AI\\database\\Screenshots")
    speak("Here Is Your ScreenShot")

def TakeHindi():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        command.pause_threshold = 1
        audio = command.listen(source)

        try:
            print("Recognizing.....")
            query = command.recognize_google(audio,language='hi')
            print(f"You Said : {query}")

        except:
            return "none"

        return query.lower()


def Tran():
    speak("Tell Me The Line!")
    line = TakeHindi()
    traslate = Translator()
    result = traslate.translate(line)
    Text = result.text
    speak(Text)


def Reader():
    speak("Tell Me The Name Of The Book!")
    name = takeCommand()

    if 'india' in name:

        os.startfile('E:\\Kaushik Shresth\\Books\\Social Science\\History\\ch 1.pdf')
        book = open('E:\\Kaushik Shresth\\Books\\Social Science\\History\\ch 1.pdf','rb')
        pdfreader = PyPDF2.PdfFileReader(book)
        pages = pdfreader.getNumPages()
        speak(f"Number Of Pages In This Books Are {pages}")
        speak("From Which Page I Have To Start Reading ?")
        numPage = int(input("Enter The Page Number :"))
        page = pdfreader.getPage(numPage)
        text = page.extractText()
        speak("In Which Language , I Have To Read ?")
        lang = takeCommand()

        if 'hindi' in lang:
            transl = Translator()
            textHin = transl.translate(text,'hi')
            textm = textHin.text
            speech = gTTS(text = textm )
            try:
                speech.save('book.mp3')
                playsound('book.mp3')

            except:
                playsound('book.mp3')

        else:
            speak(text)

    elif 'europe' in name:
        os.startfile('E:\\Kaushik Shresth\\Books\\Social Science\\History\\ch 3.pdf')
        book = open('E:\\Kaushik Shresth\\Books\\Social Science\\History\\ch 3.pdf','rb')
        pdfreader = PyPDF2.PdfFileReader(book)
        pages = pdfreader.getNumPages()
        speak(f"Number Of Pages In This Books Are {pages}")
        speak("From Which Page I Have To Start Reading ?")
        numPage = int(input())
        page = pdfreader.getPage(numPage)
        text = page.extractText()
        speak("In Which Language , I Have To Read ?")
        lang = takeCommand()

        if 'hindi' in lang:
            transl = Translator()
            textHin = transl.translate(text,'hi')
            textm = textHin.text
            speech = gTTS(text = textm )
            try:

                speech.save('book.mp3')
                playsound('book.mp3')

            except:
                playsound('book.mp3')

        else:
            speak(text)

def CloseAPPS():
    speak("Ok Sir , Wait A second!")

#    if 'youtube' in query:
 #       os.system("TASKKILL /F /im Chrome.exe")


    speak("Your Command Has Been Succesfully Completed!")

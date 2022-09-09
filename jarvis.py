import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import os
import smtplib
import requests
import  pyperclip
import datetime
from datetime import date
import pafy
import pywhatkit
from keyboard import press
from pyautogui import click
from keyboard import press_and_release
#from Features import  *
from keyboard import write
from time import sleep
import webbrowser as web
from pywikihow import search_wikihow
from playsound import playsound
import random
import json
import pyjokes
import torch
from Brain import NeuralNet
from Train import FILE
from NeuralNetwork import bag_of_words, tokenize
import sys

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json",'r') as json_data:
    intents = json.load(json_data)
FILE = "TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

#-------------
Name = "Jarvis"


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

#    speak("I am Jarvis Sir. Please tell me how may I help you")

def TaskExe():
    speak("Hello, I am Jarvis Sir.")
    speak("What's The Task Sir")

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

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('chouhanharsh256@gmail.com', 'Harsh123@')
    server.sendmail( to, content)
    server.close()

def Main():
    query = takeCommand()
    if query == "bye":
        exit()

    query = tokenize(query)
    X = bag_of_words(query, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                reply = random.choice(intent["responses"])
                speak(reply)

if __name__ == "__main__":
    wishMe()

    while True:

        Main()
        query = takeCommand().lower()

        if 'wikipedia' in query:
            try:
	            speak('Searching Wikipedia...')
	            query = query.replace("wikipedia", "")
	            results = wikipedia.summary(query, sentences=2)
	            speak("According to Wikipedia")
	            print(results)
	            speak(results)
            except Exception as e:
                print(e)
                speak("Not Found Related to this on wikipedia")

        elif 'alarm' in query:
            speak("Enter The Time !")
            time = input(": Enter The Time :")

            while True:
                Time_Ac = datetime.datetime.now()
                now = Time_Ac.strftime("%H:%M:%S")

                if now == time:
                    speak("Time To Wake Up Sir!")
                    playsound('iron.mp3')
                    speak("Alarm Closed!")

                elif now>time:
                    break

        elif 'repeat my word' in query:
            speak("Speak Sir!")
            jj = takeCommand()
            speak(f"You Said : {jj}")

        elif 'joke' in query:
            get = pyjokes.get_joke()
            speak(get)
            print(get)


        elif 'where is' in query:
            from Automations import GoogleMaps
            Place = query.replace("where is","")
#            Place = Place.replace("jarvis", "")
            GoogleMaps(Place)

        elif 'temperature in' in query:
            from Features import Temp
            Temp(query)


        elif 'IP address' in query:
            from Features import ipAddress
            ipAddress()

        elif 'shutdown my computer' in query:
            from Features import shutdown
            shutdown()

        elif 'read pdf' in query:
            from Features import pdfreader
            Place = query.replace("read pdf","")
            pdfreader(pdfreader)

        elif 'youtube download video' in query:
            from Features import youtube_video_download
            youtube_video_download()

        elif 'download youtube playlist' in query:
            from Features import download_youtube_playlist
            download_youtube_playlist()

        elif 'youtube download audio' in query:
            from Features import youtube_audio
            youtube_audio()

        elif 'play music' in query:
            music_dir = 'C:\\Users\\admin\\Downloads\\Telegram Desktop'
            songs = os.listdir(music_dir)
            print(songs)
            speak("Which music sir")
            music = takeCommand()
            os.startfile(os.path.join(music_dir, songs[music]))

        elif 'about' in query:
            from Automations import papersummary
          #  print('What to Search sir ?')
           # speak('What to search Sir ?')
            name = query.replace("about", "")
            NameA = str(name)
           # search = takeCommand()
            papersummary(NameA)

        elif 'my location' in query:
            from Features import My_Location
            My_Location()

        elif 'computer' in query:
            try:
                Path = "computer"
                os.startfile(Path)
                Path1 = os.listdir(Path)
                print(Path1)
                #   Path = takeCommand()
            except Exception as e:
                print(e)
                speak("Computer has been opened")

        elif 'control panel' in query:
            try:
                Path = "Control Panel"
                os.startfile(Path)
                Path1 = os.listdir(Path)
                print(Path1)
                #   Path = takeCommand()
            except Exception as e:
                print(e)
                speak("Control Panel has been opened")


        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("Who To Send This Email Sir")
                to = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry bhai. I am not able to send this email")



        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")



# Controling jarvis
        elif 'take a break' in query:
            speak("Ok Sir ,  You Can Call Me Anytime !")
            speak("You Just need to Say Wake Up")            
            break
            sys.exit()
            
        elif 'wait' in query:
            speak('waiting sir')
            sleep(30)

        elif 'jarvis' in query:
            speak("Yes Sir")

        elif 'how are you' in query:
            speak('i am Fine sir')

        elif 'are you listening' in query:
            speak('yes sir i am listening')

        elif 'who are you' in query:
            speak('I am a AI robot created by Harsh Chouhan')

        elif 'love you' in query:
            speak('love you too Sir')
#My Details
        elif 'pan card' in query:
            print('d')
            speak('d')

        elif 'atm' in query:
            print('Card number')
            speak('Sir Your ATM Card Number is ')

        elif 'CVV' in query:
            speak('668')

        elif 'Aadhar' in query:
            speak('Aadhar')



#windows desktop shortcuts
        elif 'side' in query:
            press_and_release('Tab')

        elif 'switch window' in query:
            press_and_release('Ctrl + Alt + Tab')

        elif 'type google' in query:
            speak('what to search sir?')
            query = takeCommand()
            write(query)

        elif 'right' in query:
            press_and_release('>')

        elif 'left' in query:
            press_and_release('<')

        elif 'up' in query:
            press_and_release('up')

        elif 'down' in query:
            press_and_release('down')

        elif 'click' in query:
            press_and_release('Enter')

        elif 'Open Task Manager' in query:
            press_and_release('Ctrl + Shift + Esc')

        elif 'switch taskbar' in query:
            press_and_release('start')

        elif 'refresh' in query:
            press_and_release('F5')

        elif 'view the previous folder' in query:
            press_and_release('Alt + <')

        elif 'view the parent folder' in query:
            press_and_release('Alt + ↑')

        elif 'Undo a change' in query:
            press_and_release('Ctrl + Z')

        elif 'Cancel selection' in query:
            press_and_release('Esc')

        elif 'View a note in full-screen mode' in query:
            press_and_release('Ctrl + Shift + C')

        elif 'Left Alt + left Shift + Print Screen' in query:
            press_and_release('Alt + <')

        elif 'view the parent folder' in query:
            press_and_release('Alt + ↑')

        elif 'Undo a change' in query:
            press_and_release('Ctrl + Z')

        elif 'Cancel selection' in query:
            press_and_release('Esc')

        elif 'View a note in full-screen mode' in query:
            press_and_release('Ctrl + Shift + C')

        elif 'open setting' in query:
            press_and_release('windows + i')

        elif 'display and Hide Desktop' in query:
            press_and_release('windows + d')

        elif 'open file explorer' in query:
            press_and_release('windows + e')

        elif 'open clipboard bin' in query:
            press_and_release('windows + ps')

        elif 'open emoji panel' in query:
            press_and_release('windows + ;')

        elif 'screenshot' in query:
            press_and_release('windows + shift + s')


#Chrome Functions
        elif 'open all the previous' in query:
            speak('Opening Previous Tabs')
            press_and_release('Ctrl + Shift + t')
            

        elif 'switch tab' in query:
            press_and_release('ctrl + t')
            speak("To Which Tab ?")
            tab = takeCommand()
            Tab = str(tab)

            if '1' in Tab:
                press_and_release('ctrl + 1')

            elif '2' in Tab:
                press_and_release('ctrl + 2')

            elif '3' in Tab:
                press_and_release('ctrl + 3')

            elif '4' in Tab:
                press_and_release('ctrl + 4')

            elif '5' in Tab:
                press_and_release('ctrl + 5')

            elif '6' in Tab:
                press_and_release('ctrl + 6')

            elif '7' in Tab:
                press_and_release('ctrl + 7')

            elif '8' in Tab:
                press_and_release('ctrl + 8')

            elif '9' in Tab:
                press_and_release('ctrl + 9')

        elif 'new tab' in query:
            press_and_release('ctrl + t')

        elif 'scroll down' in query:
            speak('scrolling in down')
            press_and_release('Space')

        elif 'scroll up' in query:
            speak('Scrolling Up')
            press_and_release('Shift + Space')

        elif 'forward' in query:
            press_and_release('Tab')

        elif 'backward' in query:
            press_and_release('Shift + Tab')

        elif 'Go to the top of the page' in query:
            speak('Top of the page')
            press_and_release('Home')

        elif 'new tab' in query:
            press_and_release('ctrl + t')

        elif 'next tab' in query:
            press_and_release('Ctrl + Tab')

        elif 'previous tab' in query:
            press_and_release('Ctrl + Shift + Tab')

        elif 'previous page' in query:
            press_and_release('Alt + <')

        elif 'next page' in query:
            press_and_release('Alt + >')

        elif 'close the tab' in query:
            press_and_release('Ctrl + w')

        elif 'new window' in query:
            press_and_release('ctrl + n')

        elif 'close the window' in query:
            press_and_release('Ctrl + Shift + w')

        elif 'minimize window' in query:
            press_and_release('windows + down')

        elif 'maximize window' in query:
            press_and_release('windows + up')

        elif 'quit chrome' in query:
            press_and_release('Alt + f + x')

        elif 'bookmark' in query:
            press_and_release('Ctrl + Shift + b')

        elif 'download' in query:
            press_and_release('Ctrl + j')

        elif 'history' in query:
            press_and_release('Ctrl + h')

        elif 'Log in from different id' in query:
            press_and_release('Ctrl + Shift + m')

        elif 'Reload page' in query:
            press_and_release('Ctrl + r')

        elif 'open' in query:
            name = query.replace("open", "")
            NameA = str(name)

            if 'YouTube' in NameA:
                web.open("https://www.youtube.com/")

            elif 'instagram' in NameA:
                web.open("https://www.instagram.com/")

            elif 'fiverr' in NameA:
                web.open("https://www.fiverr.com/users/harshchouhan683/seller_dashboard")

            elif 'WhatsApp' in NameA:
                web.open("https://web.whatsapp.com/")

            elif 'Twitter' in NameA:
                web.open("https://twitter.com/")
            
            elif 'a w s' in NameA:
                web.open("https://aws.amazon.com/")

            elif 'stockedge' in NameA:
                web.open("https://web.stockedge.com/scan-groups")

            elif 'Moneycontrol' in NameA:  
                web.open("https://www.moneycontrol.com/")    

            elif 'nse' in NameA:
                web.open("https://www.nseindia.com/")

            elif 'amazon' in NameA:
                web.open(
                    "https://www.amazon.in/gp/css/order-history?ie=UTF8&ref_=nav_orders_first&openid.assoc_handle=inamazon&openid.claimed_id=https%3A%2F%2Fwww.amazon.in%2Fap%2Fid%2Famzn1.account.AEETCB2JAGLR76YZJCIHHHJ7RCVA&openid.identity=https%3A%2F%2Fwww.amazon.in%2Fap%2Fid%2Famzn1.account.AEETCB2JAGLR76YZJCIHHHJ7RCVA&openid.mode=id_res&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.op_endpoint=https%3A%2F%2Fwww.amazon.in%2Fap%2Fsignin&openid.response_nonce=2021-09-15T04%3A51%3A22Z7013071818977553626&openid.return_to=https%3A%2F%2Fwww.amazon.in%2Fgp%2Fcss%2Forder-history%3Fie%3DUTF8%26ref_%3Dnav_orders_first&openid.signed=assoc_handle%2Cclaimed_id%2Cidentity%2Cmode%2Cns%2Cop_endpoint%2Cresponse_nonce%2Creturn_to%2Cns.pape%2Cpape.auth_policies%2Cpape.auth_time%2Csigned&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.auth_policies=AmazonMultifactor&openid.pape.auth_time=2021-09-15T04%3A51%3A22Z&openid.sig=Dg0wAADc%2BkQxG9SokBzHDWckQerVYfFFX1YMpDv9YKQ%3D&serial=&")

            elif 'tradingview' in NameA:
                web.open("https://in.tradingview.com/chart/")

            elif 'screener' in NameA:
                web.open("https://www.screener.in/dash/#")

            elif 'investing' in NameA:
                web.open("https://in.investing.com/")

            elif 'top contracts' in NameA:
                web.open("https://www.nseindia.com/market-data/equity-derivatives-watch")

            elif 'angel broking' in NameA:
                web.open("https://trade.angelbroking.com/Login?RetUrl=/portfolio/equity/index_v1")

            else:
                string = "https://www." + NameA + ".com"
                string_2 = string.replace(" ", "")
                web.open(string_2)


        elif 'google search' in query:
            press_and_release('Ctrl + k')
            speak('what to search sir?')
            query = takeCommand()
            write(query)
            press('enter')
            speak(f'Searching {query} on Google')

        elif 'write' in query:
            speak("what to write sir?")
            time = takeCommand()
            write(time)
            press_and_release('enter')
            speak(f'writing {time}')


# YouTube Shortcuts
        elif 'search on YouTube' in query:
            name = query.replace("search on YouTube", "")
            NameA = str(name)
            from Features import YouTubeSearch
            YouTubeSearch(NameA)

        elif 'YouTube search' in query:
            press_and_release('?')
            press_and_release('Ctrl + a')
            speak('what to search on youtube sir?')
            query = takeCommand()
            write(query)
            press('enter')
           

            # k = space bar

        elif 'YouTube music playlist' in query:
            web.open('https://www.youtube.com/playlist?list=PLLE_ohvTS98nq85oGjX-mEC8oEoUbSlL6')

        elif 'restart' in query:
            press('0')

        elif 'stop'in query:
            press('k')

        elif 'resume' in query:
            press('k')

        elif 'full screen' in query:
            press('f')

        elif 'film screen' in query:
            press('t')

        elif 'skip' in query:
            press('l')
            speak('Skipping the video')

        elif 'back' in query:
            press('j')
            speak('taking back video')

        elif 'subtitle' in query:
            press('c')

        elif 'open miniplayer' in query:
            press_and_release('i')

        elif 'previous video' in query:
            press_and_release('Shift+p')

        elif 'next video' in query:
            press_and_release('Shift+N')

        elif 'increase volume' in query:
            press_and_release('up')

        elif 'decrease volume' in query:
            press_and_release('down')

        elif 'mute' in query:
            press_and_release('m')

        elif 'subtitle' in query:
            press_and_release('c')



#Trading view shortcuts

        elif 'change time period to' in query:
            name = query.replace("change time period to", "")
            query = str(name)
            write(query)
            press_and_release('enter')
            speak(f'changing time period to {query}')

#Zerodha Shortcuts
        elif 'dashboard' in query:
            press_and_release('a')

        elif 'orders' in query:
            press_and_release('o')

        elif 'holdings' in query:
            press_and_release('h')

        elif 'positions' in query:
            press_and_release('p')

        elif 'funds' in query:
            press_and_release('f')

        elif 'profile' in query:
            press_and_release('i')

        elif 'edit profile' in query:
            press_and_release('j')

        elif 'keyboard shortcuts' in query:
            press_and_release('?')

        elif 'cycle through instruments' in query:
            press_and_release('down')

        elif 'buy' in query:
            press_and_release('b')
            speak('how much quantity sir ?')
            qnty = takeCommand()
            write(qnty)

        elif 'stock search' in query:
            press_and_release("`")


        elif 'sell' in query:
            press_and_release('s')

        elif 'open market depth' in query:
            press_and_release('d')

        elif 'open chart' in query:
            press_and_release('c')

        elif 'delete' in query:
            press_and_release('delete')

        elif 'switch marketwatch' in query:
            speak('which number sir')
            no = takeCommand()
            press_and_release(f'Ctrl + Shift + {no}')

        elif 'Buy opened chart' in query:
            press_and_release('b')

        elif 'Sell opened chart' in query:
            press_and_release('s')

        elif 'Toggle quick trade drawer' in query:
            press_and_release('Ctrl + Shift + z')



#Nasa
        elif 'space news' in query:
            speak("For Which Date?")
     #Date Format= year-month-day
            Date = takeCommand()
            from Features import DateConverter
            value = DateConverter(Date)
            from nasa import NasaNews
            NasaNews(value)

        elif 'details of planet' in query:
            speak("For Which planet sir?")
     #Date Format= year-month-day
            planet = takeCommand()
            NasaNews(planet)


#Opening computer Apps
        elif 'chrome' in query:
            codePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(codePath)
            press_and_release('Ctrl + Shift + t')
            speak('Chrome has opened')


        elif 'telegram' in query:
            codePath = "C:\\Users\\admin\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"
            speak('Opening Telegram')
            os.startfile(codePath)
            speak('Telegram has opened')

        elif 'zoom' in query:
            codePath = "C:\\Users\\admin\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
            os.startfile(codePath)
            speak('zoom app has opened')

        elif 'command line' in query:
            codePath = "%windir%\\system32\\cmd.exe"
            os.startfile(codePath)
            speak('command line has opened')

        elif 'Visual Studio' in query:
            codePath = "C:\\Users\\admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            speak('opening Visual Studio')
            os.startfile(codePath)
             
        elif 'sublime' in query:
            codePath = "C:\\Program Files\\Sublime Text 3\\sublime_text.exe"
            speak('opening sublime')
            os.startfile(codePath)

        elif 'pycharm' in query:
            codePath = "C:\\Program File\\PyCharm Community Edition 2020.2.3\\bin\\pycharm64.exe"
            speak('opening Pycharm')
            os.startfile(codePath)

def whatsappMsg(name,message):
    click()
    sleep(1)
    write(name)
    sleep(0.5)
    click()
    sleep(0.5)
    write(message)


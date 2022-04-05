import requests
import os
from PIL import Image
import pyttsx3
from datetime import datetime
#import cartopy.crs as ccrs
#import matplotlib.pyplot as plt
from keyboard import press
from pyautogui import click
from keyboard import press_and_release
#from features import GoogleSearch
from keyboard import write
from time import sleep
import webbrowser as web
from jarvis import takeCommand
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def GoogleMaps(Place):
    Url_Place = "https://www.google.com/maps/place/" + str(Place)

    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(Place , addressdetails=True)
    target_latlon = location.latitude, location.longitude

  #  web.open(url=Url_Place)

    location = location.raw['address']
    target = {'city' : location.get('city', ''),
              'state' : location.get('state',''),
              'country' : location.get('country','')}
    current_loca = geocoder.ip('me')
    current_latlon = current_loca.latlng
    distance = str(great_circle(current_latlon, target_latlon))
    distance = str(distance.split(' ',1)[0])
    distance = round(float(distance),2)

   # speak(target)
    print(f"Sir , {Place} is {distance} Kilometer Away From Your Location and it is located in {target} ")
    speak(f"Sir , {Place} is {distance} Kilometer Away From Your Location and it is located in {target} ")



from newspaper import Article
from sumy.utils import get_stop_words
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from jarvis import takeCommand, speak

LANGUAGE = "english"
def papersummary(search):
    # configurable number of sentences
    SENTENCES_COUNT = 10

    article = Article(
        f'https://www.google.com/search?q=+{search}')
    article.download()
    article.parse()

    # text cleaning
    text = "".join(article.text).replace("\n", " ").replace('"', "").replace(
        "• Follow the Long Read on Twitter at @gdnlongread, and sign up to the long read weekly email here.", "")

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    article_summary = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        article_summary.append(str(sentence))

    clean_summary = ' '.join([str(elem) for elem in article_summary])
    print(clean_summary)
    speak(clean_summary)


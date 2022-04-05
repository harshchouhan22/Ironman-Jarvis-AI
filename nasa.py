import requests
import os
from PIL import Image
import pyttsx3
from datetime import datetime
#import cartopy.crs as ccrs
#import matplotlib.pyplot as plt
Api_key = "9ap7eXXWwVfBPT1wYY6rbgORlRHGhMqYuHt9ktgB"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# print(voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def NasaNews(Date):

    speak("Extracting Data From Nasa")

    url = "https://api.nasa.gov/planetary/apod?api_key=" + str(Api_key)
    Params = {'date':str(Date)}

    r = requests.get(url,params = Params)

    Data = r.json()
    Info = Data['explanation']
    Title = Data['title']
    Image_Url  = Data['url']
    Image_r = requests.get(Image_Url)
    FileName = str(Date) + '.jpg'
    with open(FileName, 'wb') as f:
        f.write(Image_r.content)

    Path_1 = "F:\\Python AI\\" + str(FileName)
    Path_2 = "F:\\Python AI\\database\\nasa_images\\" + str(FileName)
    os.rename(Path_1, Path_2)
    img = Image.open(Path_2)
    img.show()
    speak(f"Title : {Title}")
    speak(f"According To Nasa : {Info}")

def IssTracker():
    url = "http://api.open-notify.org/iss-now.json"
    r = requests.get(url)
    Data = r.json()
    dt = Data['timestamp']
    lat = Data['iss_position']['latitude']
    lon = Data['iss_position']['longitude']

    print(f"Time And Date : {dt}")
    print(f"Latitude : {lat}")
    print(f"Longitude : {lon}")

 #   plt.figure(figsize=(10,8))
#    ax = plt.axis(projection = ccrs.PlateCarree())
 #   ax.stock_img()
  #  plt.scatter(float(lon), float(lat),color = 'blue' , marker='o')
   # plt.show()


def SolarBodies(body):
    url = "https://api.le-systeme-solaire.net/rest/bodies/"
    r = requests.get(url)
    Data = r.json()
    bodies = Data['bodies']

    Number = len(bodies)
    for bodyyy in bodies:
        print(bodyyy['id'],end=',')

    url_2 = f"https://api.le-systeme-solaire.net/rest/bodies/{body}"
    rrr = requests.get(url_2)
    data_2 = rrr.json()

    mass = data_2['mass']['massValue']
    volume = data_2['vol']['volValue']
    density = data_2['density']
    gravity = data_2['gravity']
    escape = data_2['escape']

    speak(f"Number Of Bodies In Solar System : {Number}")
    speak(f"Mass Of {body} Is {mass}")
    speak(f"Gravity Of {body} Is {gravity}")
    speak(f"Escape Velocity Of {body} Is {escape}")
    speak(f"Density Of {body} Is {density}")

    print(data_2)

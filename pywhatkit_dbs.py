from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--window-size=1024x768")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('F:\\chromedriver.exe')





def ask_google(query):

    # Search for query
    query = query.replace(' ', '+')

    driver.get('http://www.google.com/search?q=' + query)

    # Get text from Google answer box

    answer = driver.execute_script(
            "return document.elementFromPoint(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5]);",
            626.97, 89).text
    answer1 = driver.execute_script(
            "return document.elementFromPoint(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5]);",
            652, 89).text
    print(answer1)
    print(answer)
    return answer

#ask_google("who is elon musk")
import newspaper
def paper():
    url = "https://www.google.com/search?q=elon+musk&oq=&sourceid=chrome&ie=UTF-8"
    url_i = newspaper.Article(url="%s" % (url), language='en')
    url_i.download()
    url_i.parse()
    print(url_i.text)
#paper()

# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog


# Function for opening the
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)

def exp():
    # Create the root window
    window = Tk()

    # Set window title
    window.title('File Explorer')

    # Set window size
    window.geometry("500x500")

    # Set window background color
    window.config(background="white")

    # Create a File Explorer label
    label_file_explorer = Label(window,
                                text="File Explorer using Tkinter",
                                width=100, height=4,
                                fg="blue")

    button_explore = Button(window,
                            text="Browse Files",
                            command=browseFiles)

    button_exit = Button(window,
                         text="Exit",
                         command=exit)

    # Grid method is chosen for placing
    # the widgets at respective positions
    # in a table like structure by
    # specifying rows and columns
    label_file_explorer.grid(column=1, row=1)

    button_explore.grid(column=1, row=2)

    button_exit.grid(column=1, row=3)

    # Let the window wait for any events
    window.mainloop()
exp()
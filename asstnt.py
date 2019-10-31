# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 00:18:32 2019

@author: BALAKA
"""
import pyttsx3
import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
# import vlc
import urllib.request
import urllib3
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime


# Function to get user commands
def Command():
    rec = sr.Recognizer()                   # Recognizes every speech that I say
    with sr.Microphone() as source:         # Use default microphone as audio input
        print('Say...')
        rec.pause_threshold = 1             # Pause for 1 second
        rec.adjust_for_ambient_noise(source, duration = 1)      # Listens to calibrate for ambient noise levels
        audio = rec.listen(source)          # Listens for the 1st phrase and extract it into audio data
    try:
        command = rec.recognize_google(audio).lower()   # Recognize speech using Google Recognition
        print('You just said : ' + command + '\n')        # Print my command
        
# We go back into the loop to continue listening for commands if speech is not understandable.

    except sr.UnknownValueError:
        print('...')                    # If speech is unintelligible, print ...
        command = Command()            # Loop back to take another command
    return command


'''def Shutdown():
    print("GoodBye for now ! Have a nice day !")
    sys.exit()'''


# Function to respond
def Response(audio):
    s = pyttsx3.init()              # Initialize the tts converter
    sound = s.getProperty('voices')
    s.setProperty('voice', sound[1].id)
    s.say(audio)                    # Converts the text to audio
    s.runAndWait()                  # Last step: playing the audio
    print(audio)


# command()
# Actual function for executing commands starts

# Function to give work to assistant
def asstnt(commnd):
    # 1. Greet/Leave

    # a. Greet
    if 'hello' in commnd:
        Response("Hey there ! What do I call you ?")
        name = Command()

        # Time constraints
        c_time = int(strftime('%H'))
        if c_time < 12:
            Response("Good Morning %s! That's a lovely name !" % (name))
        elif c_time >= 12 and c_time < 17:
            Response("Good Afternoon %s!" % (name))
        else:
            Response("Good Evening %s! I was missing you !" % (name))

    # b. Shut down
    elif 'bye' in commnd or 'sleep' in commnd:
        Response("Bye bye ! Have an awesome day !")
        sys.exit()

    # 2. Open Google Chrome
    elif 'open google' in commnd:
        url = "https://www.google.com/"
        webbrowser.open(url)                        # webbrowser.open() opens any website defined by user
        Response("Google Chrome has been opened for you ! Enjoy Browsing")          # Assistant's reply
    # 3. Open any website
    elif 'open' in commnd:
        x = re.search('open (.+)', commnd)          # Search for the word open
        if x:
            domain_name = x.group(1)                # The second phrase in the speech has to be the domain name
            url = 'https://www.' + domain_name      # Define the url
            webbrowser.open(url)                    # Open it
            Response("The website you asked for has been opened for you !")       # Assistant's reply
    # 4. Show current weather and temperature
    elif 'current weather' in commnd:
        x = re.search("current weather (.*)", commnd)       # Search command for the phrase current weather
        if x:                                               # If true
            city = x.group(1)                               # Get the name of the city
            owm = OWM(API_key= 'ab0d5e80e8dafb2cb81fa9e82431c1fa')      # API key
            obs = owm.weather_at_place(city)                            # Use weather_at_place() to obtain the info
            w = obs.get_weather()                                       # Use get_weather() for the weather components
            k = w.get_status()                              # Use get_status() to get status of current weather
            t = w.get_temperature(unit= 'celsius')          # Use get_temperature(unit of temperature) to get the temperature
            Response("Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius" % (city, k, t['temp_max'], t['temp_min']))
    # 5. Tell current time
    elif 'time' in commnd:
        import datetime
        nw = datetime.datetime.now()
        Response("The current time is %d hours and %d minutes" % (nw.hour, nw.min))

    # 6. Latest news
    elif 'today\'s news' in commnd:
        try:
            news = "https://news.google.com/news/rss"
            c = urlopen(news)                                   # Open Google news
            read = c.read()                                     # Read them and store
            c.close()
            s_page = soup(read, "xml")                          #
            n_lst = s_page.findAll("item")
            for n in n_lst[:15]:                                # First 15 news
                Response(n.title.text.encode('utf-8'))
        except Exception as ex:
            print(ex)

    # 7. Inform you about anything
    elif 'tell me about' in commnd:
        r = re.search('tell me about (.*)', commnd)
        try:
            if r:




# asstnt(Command())

'''import os

cmd = 'notepad'
os.system(cmd) '''
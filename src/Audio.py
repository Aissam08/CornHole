# importing speech recognition package from google api
import speech_recognition as sr 
import playsound # to play saved mp3 file
from gtts import gTTS # google text to speech
import os # to save/open files
#import wolframalpha # to calculate strings into formula
from selenium import webdriver # to control browser operations
import pygame
# import vlc
import urllib.request
import urllib.parse
import urllib.error


num = 1
def assistant_speaks(output):
    global num
  
    # num to rename every audio file 
    # with different name to remove ambiguity
    num += 1
    #print("PerSon : ", output)
  
    toSpeak = gTTS(text = output, lang ='en', slow = False)
    # saving the audio file given by google text to speech
    file = str(num)+".mp3"
    toSpeak.save(file)
      
    # playsound package is used to play the same file.
    playsound.playsound(file, True) 
    os.remove(file)
  
  
  
def get_audio():
  
    rObject = sr.Recognizer()
    audio = ''
  
    with sr.Microphone() as source:
        print("Speak...")
          
        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit = 3) 
    #print("Stop.") # limit 5 secs
  
    try:
        text = rObject.recognize_google(audio, language ='en-US')
        print("You : ", text)
        return text
  
    except:
       # assistant_speaks("Could not understand your audio, PLease try again !")
        return ""



#-- Connect to nabastag
def send_request(message):
    # try:
    #     request = urllib.request.urlopen("http://192.168.1.57:7899/{}".format(message))
    # except :
    #     print("Error connexion nabaztag")
    #     pass
    pass

#-- Requêtes Nabaztag
"""
blackstart
whitestart
1pointblack
1pointwhite
3pointblack
3pointwhite
blackwon
whitewon
"""
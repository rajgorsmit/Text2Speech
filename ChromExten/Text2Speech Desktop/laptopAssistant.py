from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import weather_api as Weather
import win32com.client as wincl
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import *

speak = wincl.Dispatch("SAPI.SpVoice")

root = Tk()

def talkToMe(audio):
    print(audio)
    speak.Speak(audio)

def GetWebData(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()    

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    talkToMe(text)

def myCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        speak_command = 'Please give some command to me...'
        talkToMe(speak_command)
        
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        talkToMe('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        talkToMe('Your last command couldn\'t be heard ! I can understand commands like send email, open gmail, open website xyz.com and tell me a joke')
        #speak.Speak('Your last command couldn\'t be heard')
        command = myCommand()

    return command


def assistant(command):    
    #"if statements for executing commands"
    message = 'Speak'

    if 'start' in command:
        talkToMe(message)

    elif 'website' in command:
        url = input(":")
        GetWebData(url)
    
    elif 'stop' in command:
        talkToMe(message)

    elif 'end' in command:
        talkToMe(message)
    
    elif 'resume' in command:
        talkToMe(message)

    elif 'restart' in command:        
        talkToMe('Done!')

    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            talkToMe('Done!')
            GetWebData(url)
        else:
            pass

    elif 'open notepad' in command:
        os.system('notepad')
        talkToMe('Done for you!')

    elif 'whats up' in command:
        talkToMe('Just doing my thing')

    elif 'tell me a joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe('Here is an awesome joke for you- ')
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')

    #this option is not funtioning as proxy need to set to bypass HMCL IT settings
    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.+)', command)
        talkToMe(reg_ex)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            condition = location.condition()
            talkToMe('The Current weather in %s is %s The temperature is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))
        else:
            talkToMe("City name not fetched")

    #this option is not funtioning as proxy need to set to bypass HMCL IT settings
    elif 'weather forecast in' in command:
        reg_ex = re.search('weather forecast in (.+)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            forecasts = location.forecast()
            for i in range(0,3):
                talkToMe('On %s will it %s. The maximum temperture will be %.1f degree.'
                         'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))


    elif 'send email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()
        receiver = False

        if 'john' in recipient:
            receiver = "receiversemail"
        
        else:
            talkToMe('I am not able to fetch receiver name buddy! ')
        
        if receiver:

            talkToMe('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('youremail.com', 'password')

            #send message
            mail.sendmail('Testing Desktop assistant', receiver, content)

            #end mail connection
            mail.close()

            talkToMe('Email sent.')
        
        else:
            talkToMe('Buddy I am not sending email ! you failed to provide me a receiver name')
        

    elif 'bye' in command:
        talkToMe('See you later Take care !')
        exit()

    else:
            talkToMe('I don\'t know what you mean! I can understand commands like send email, open gmail, open website xyz.com and tell me a joke, website')

talkToMe('Hey, I am your laptop\'s Jarvis and I am ready for your command !')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
   

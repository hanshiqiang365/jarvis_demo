#author: hanshiqiang365 （微信公众号：韩思工作室）

import time
import os
import pyaudio
import wave
import speech_recognition as sr
from aip import AipSpeech
import requests
import json
from playsound import playsound

# Baidu Speech API, replace with your personal key
APP_ID = 'XXXXXXXXXXXXXXX'
API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXX'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# Turing API, replace with your personal key
TURING_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
URL = "http://openapi.tuling123.com/openapi/api/v2"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}


# Use SpeechRecognition to record
def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("Please start talking")
        audio = r.listen(source)

    with open("voices/recording.wav", "wb") as f:
        f.write(audio.get_wav_data())


# Use Baidu Speech as STT engine
def listen():
    with open('voices/recording.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1536,
    })

    result_text = result["result"][0]
    print("You said: " + result_text)
    return result_text


# The Turing chatbot
def robot(text=""):
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": ""
            },
            "selfInfo": {
                "location": {
                    "city": "大连",
                    "street": "凌水路"
                }
            }
        },
        "userInfo": {
            "apiKey": TURING_KEY,
            "userId": "starky"
        }
    }

    data["perception"]["inputText"]["text"] = text
    response = requests.request("post", URL, json=data, headers=HEADERS)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI said: " + result)
    return result


# Baidu Speech as TTS engine
def speak(text,filename):
    result = client.synthesis(text, 'zh', 1, {
        'spd': 4,
        'vol': 5,
        'per': 4,
    })

    with open(filename, 'wb') as f:
        f.write(result)

# Play mp3 file
def play(filename):
    playsound(filename)

filenumber = 0
final_text = ""

while True:
    rec()
    request = listen()
    response = robot(request)

    audiofile = f"voices/audio0{filenumber}.mp3"
    
    speak(response,audiofile)
    play(audiofile)

    final_text = final_text + "You said: " + str(request) +"\r\n"
    final_text = final_text + "AI said: " + str(response) +"\r\n"
    
    filenumber = filenumber + 1

    if request == "结束":
        break

with open(f'jarvis_talk.txt', 'wb') as txt_f:
        txt_f.write(final_text.encode('utf-8'))

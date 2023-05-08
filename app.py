from __future__ import division, print_function

from flask import Flask,render_template,url_for,request

from flask_bootstrap import Bootstrap


import os
from flask_mysqldb import MySQL
import yaml
import random
import string
import time
import pyttsx3
import speech_recognition as sr



app = Flask(__name__)

Bootstrap(app)
with open('db.yaml') as f:
    
    db = yaml.load(f, Loader=yaml.FullLoader)
   
    app.config['MYSQL_HOST'] = db['mysql_host']
    app.config['MYSQL_USER'] = db['mysql_user']
    app.config['MYSQL_PASSWORD'] = db['mysql_password']
    app.config['MYSQL_DB'] = db['mysql_db']
    mysql = MySQL(app)

@app.route('/', methods=['GET'])

def index():
    return render_template('questions.html')

@app.route('/fetch_questions')

def fetch_questions():
    cur1 = mysql.connection.cursor()
        
    result1 = cur1.execute("SELECT questions, options, option1, option2, answer FROM questions")
    if(result1>0):
        questions = cur1.fetchall()
        # Create a cursor object to execute SQL queries
        
        
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()
        
        # Initialize the speech recognition engine
        r = sr.Recognizer()
        
        # Set the voice rate (higher value means faster speaking)
        
        print(questions)
        engine.setProperty('rate', 150)


        engine.setProperty('volume', 1)
        
        # Set the voice (change to a voice installed on your system)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        
        # Define a function to speak out the text
        def speak(text):
            engine.say(text)
            engine.runAndWait()
        
        # Define a function to recognize speech
        def recognize_speech():
            with sr.Microphone(device_index=1) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Speak now...")
                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio)
                    print("You said:", text)
                    return text
                except:
                    print("Sorry, I didn't catch that.")
                    return ""
        
        # Loop through the questions and ask them
        score = 0
        for q in questions:
            # Speak the question
            speak(q[0])
            print(q[0])
        
            # Speak the options
            speak("Option 1")
            speak(q[1])
            print("Option 1:", q[1])
            speak("Option 2")
            speak(q[2])
            print("Option 2:", q[2])
            speak("Option 3")
            speak(q[3])
            print("Option 3:", q[3])
           
        
            # Recognize the answer
            answer = recognize_speech()
        
            # Check if the answer is correct and speak the result
            if answer == q[4]:
                speak("Correct!")
                print("Correct!")
                score += 1
            else:
                speak("Wrong!")
                print("Wrong!")
            
            # Speak the current score
            speak("Your score is " + str(score))
            print("Your score is", score)


    return render_template('questions.html')

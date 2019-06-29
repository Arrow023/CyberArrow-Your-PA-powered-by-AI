import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import random
import cv2
faces_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[0].id)
def detect(gray, frame):
    faces=faces_cascade.detectMultiScale(gray, 1.2, 6)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2) #2 is the width of the frame lines
        font=cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Admin',(x,y),font,1,(0,255,255))
        roi_gray=gray[x:x+w,y:y+h]   # region of interest of gray like from x to x+w and y to y+h
        roi_color=frame[x:x+w,y:y+h]  #region of interest of color similar to roi_gray
    return frame                   
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour >=0 and hour<12:
        speak('Good Morning!')
    elif hour>=12 and hour<18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')
    speak('I am Cyber Arrow, your personal assistant. Please tell me what to do for you')
def sendEmail(to,content):
    file=open('mail.txt','r')
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    id=file.readline()
    passw=file.readline()
    server.login(id,passw)
    server.sendmail(id,to,content)
    server.close() 
    file.close()
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening to source.....')
        r.pause_threshold=0.5
        audio=r.listen(source)
    try:
        print('Recognizing....')
        query=r.recognize_google(audio,language='en-in')
        print(f'User said:{query}\n')
    
    except Exception as e:
        #print(e)
        print('Say it again')
        return 'None'
    return query
wishMe()
flag=True
while(flag):
    query=takeCommand().lower()
    if 'wikipedia' in query:
        speak('Searching Wikipedia.....')
        query=query.replace('wikipedia','')
        results=wikipedia.summary(query,sentences=2)
        speak('According to Wikipedia')
        speak(results)
    elif 'open youtube' in query:
        webbrowser.open('youtube.com')
    elif 'play music' in query:
        music_dir='F:\\'
        songs=os.listdir(music_dir)
        num=random.randint(1,len(songs)-1)
        #print(songs)
        os.startfile(os.path.join(music_dir,songs[num]))
    elif 'the time' in query:
        strtime=datetime.datetime.now().strftime('%H:%M:%S')
        speak(f'The time is {strtime}')
    elif 'open code' in query:
        code_path='C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
        os.startfile(code_path)
    elif 'email' in query:
        try:
            speak('What should I say...')
            content=takeCommand()
            to='kirajustice807@outlook.in'
            sendEmail(to,content)
            speak('Email has been sent...')
        except Exception as e:
            speak('Sorry I could not send email..')
    elif 'who am i' in query:
        video_capture = cv2.VideoCapture(0)
        while True:
            _,frame=video_capture.read()
            gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            canvas = detect(gray, frame)
            cv2.imshow('video', canvas) 
            if cv2.waitKey(1) & 0xFF == ord('l'): 
                break
        video_capture.release()
        cv2.destroyAllWindows() 
    elif 'quit' in query:
        flag=False      


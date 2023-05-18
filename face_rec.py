import face_recognition as fr
import os
import cv2
import pygetwindow
import pyautogui
from PIL import Image
from twilio.rest import Client
import pywhatkit
import winsound
import face_recognition
import numpy as np
from time import sleep
# from simple_facerec import SimpleFacerec

#         #encode faces from a folder
# sfr = SimpleFacerec()
# sfr.load_encoding_images("faces/")

cap =cv2.VideoCapture(0)
sid = 'ACbeba29d6ede666aa54adb39579b3630e'
authtoken = '17b7d96dea914eff96f773fb7290f81e'
client = Client(sid , authtoken)
fnumber = 'whatsapp:+14155238886'
tnumber = 'whatsapp:+254792745678'

i = 1
while True:
    ret, frame = cap.read()
    cv2.imshow('Frame', frame)
        #Detect Faces
    # face_location, face_names = sfr.detect_known_faces(frame)
    # for face_loc, name in zip(face_location, face_names):
    #      print(face_loc)
    #      y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
    
    #      cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 150), 2)
    #      cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 150), 2)
    #      winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

    key =cv2.waitKey(10)
    if key == ord('q'):
        break
    # for i in range (3, 4):
    if i == 70:
        path = 'C:\\xampp\\htdocs\\face\\intruder.png'
        # window = pygetwindow.getWindowsWithTitle('Frame')[0]
        # left, top = window.topleft
        # right, bottom = window.bottomright
        # pyautogui.screenshot(path)
        # im = Image.open(path)
        # im = im.crop((left+10, top+30, right-10, bottom-10))
        # im.save(path)
        # im.show(path)

#https://f776-197-237-50-188.eu.ngrok.io


        cv2.imwrite(path, frame)
        #pywhatkit.sendwhats_image('+254758751837', path,"This is me", 15, True, 3)
        msg = client.messages.create(body='Intruder',
                                     media_url='https://2b38-197-237-50-188.eu.ngrok.io/face/intruder.png',
                                     from_=fnumber,
                                     to=tnumber)

    i = i+1



print(msg.sid)

cap.release()
cv2.destayAllWindows()





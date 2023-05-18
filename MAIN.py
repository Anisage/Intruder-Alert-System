import face_recognition
import os, sys
from twilio.rest import Client
import cv2
import numpy as np
import math

import pyautogui
import pygetwindow
from PIL import Image
import winsound
import time



sid = 'ACbeba29d6ede666aa54adb39579b3630e'
authtoken = '17b7d96dea914eff96f773fb7290f81e'
client = Client(sid , authtoken)
fnumber = 'whatsapp:+14155238886'
tnumber = 'whatsapp:+254792745678'


def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)
        add = 1

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        while True:
            ret, frame = video_capture.read()

            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)


                rgb_small_frame = small_frame[:, :, ::-1]


                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:

                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Intruder"
                    confidence = '???'



                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])
                    else:
                        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
                        path = "C:\\Users\\Wilson Kamau\\Documents\\Enoch\\face_rec\\intruder3.png"
                        # window = pygetwindow.getWindowsWithTitle('Frame')[0]
                        # left, top = window.topleft
                        # right, bottom = window.bottomright
                        # pyautogui.screenshot(path)
                        # im = Image.open(path)
                        # im = im.crop((left + 10, top + 30, right - 10, bottom - 10))
                        # im.save(path)
                        # im.show(path)
                        if add == 1:
                            path1 = 'C:\\xampp\\htdocs\\face\\intruder.png'
                            cv2.imwrite(path1, frame) 
                            # pywhatkit.sendwhats_image('+254758751837', path,"This is me", 15, True, 3)
                            msg = client.messages.create(body='!!!!! Intruder !!!!',
                                                        media_url='https://5bd9-197-237-50-188.eu.ngrok.io/face/intruder.png',
                                                        from_=fnumber,
                                                        to=tnumber)
                            add = add+1

                    self.face_names.append(f'{name} ({confidence})')
                    if name != "Intruder":
                        add = 1

            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):

                top *= 4
                right *= 4
                bottom *= 4
                left *= 4


                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)


            cv2.imshow('Face Recognition', frame)


            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()